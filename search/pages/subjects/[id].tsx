import { GetServerSideProps, NextPage } from 'next'
import { Image, ImageSource } from '../../types/image'
import { getClient, getSubject } from '../../services/elasticsearch'

import { ArrowUpRight } from 'react-feather'
import { Concept } from '../../types/concept'
import Head from 'next/head'
import ImageResultsOverview from '../../components/results/overview/images'
import Layout from '../../components/layout'
import { Story } from '../../types/story'
import StoryResultsOverview from '../../components/results/overview/stories'
import { Work } from '../../types/work'
import WorkResultsOverview from '../../components/results/overview/works'

type Props = {
  concept: Concept
  images: Image[]
  totalImages: number
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const conceptId = query.id as string
  const client = getClient()
  const concept = await getSubject(client, conceptId)

  const capitalisedConceptName = (concept.label ? concept.label : '').replace(
    /(^\w{1})|(\s+\w{1})/g,
    (letter) => letter.toUpperCase()
  )

  const url = `https://api.wellcomecollection.org/catalogue/v2/images?source.subjects.label=${capitalisedConceptName}`
  const imageResponse = await fetch(url).then((res) => res.json())
  const images = imageResponse.results.map((image: ImageSource) => {
    return {
      id: image.source.id,
      url: image.thumbnail.url.replace('info.json', 'full/400,/0/default.jpg'),
      title: image.source.title,
    }
  })

  return { props: { concept, images, totalImages: imageResponse.totalResults } }
}

const SubjectPage: NextPage<Props> = ({ concept, images, totalImages }) => {
  const description =
    concept.wikidata_description || concept.mesh_description || null
  const capitalisedDescription = description
    ? description?.charAt(0).toUpperCase() + description?.slice(1)
    : null
  return (
    <div className="pb-8">
      <Head>
        <title>{concept.preferred_label}</title>
      </Head>
      <Layout>
        <div className="space-y-8 bg-red py-8">
          <div className="mx-auto  px-5 lg:w-3/4">
            <h1 className="font-sans text-5xl capitalize">
              {concept.preferred_label}
            </h1>
          </div>
          <div className="mx-auto flex flex-col space-y-8 px-5 lg:w-3/4 lg:flex-row lg:space-y-0 lg:space-x-12">
            <div className="space-y-4 lg:w-2/3">
              <p className="font-sans text-lg">{capitalisedDescription}</p>
              <div className="flex flex-col ">
                {concept.wikidata_id && (
                  <a
                    href={`https://www.wikidata.org/wiki/${concept.wikidata_id}`}
                  >
                    Read more on Wikidata <ArrowUpRight className="inline" />
                  </a>
                )}
                {concept.mesh_id && (
                  <a href={`https://id.nlm.nih.gov/mesh/${concept.mesh_id}`}>
                    Read more on MeSH <ArrowUpRight className="inline" />
                  </a>
                )}
                {concept.lc_subjects_id && (
                  <a
                    href={`https://id.loc.gov/authorities/subjects/${concept.lc_subjects_id}`}
                  >
                    Read more on Library of Congress (subjects)
                    <ArrowUpRight className="inline" />
                  </a>
                )}
                {concept.lc_names_id && (
                  <a
                    href={`https://id.loc.gov/authorities/names/${concept.lc_names_id}`}
                  >
                    Read more on Library of Congress (names)
                    <ArrowUpRight className="inline" />
                  </a>
                )}
              </div>
              <div>
                <p className="font-bold">Also known as</p>
                <p>
                  {concept.variants
                    .map((variant) => {
                      return (
                        variant?.charAt(0).toUpperCase() + variant?.slice(1)
                      )
                    })
                    .join(', ')}
                </p>
              </div>
            </div>
            <div className="lg:w-1/3">
              <p className="font-bold">Related subjects</p>
              <ul className="flex flex-wrap gap-x-2 pt-4 ">
                {concept.neighbours.map((neighbour) => (
                  <li key={neighbour.id} className="pb-6">
                    <a
                      className="w-100 rounded-full border border-black py-2 px-3 text-sm capitalize no-underline"
                      href={`/subjects/${neighbour.id}`}
                    >
                      {neighbour.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className="space-y-16">
          {concept.works.length > 0 && (
            <div className="mx-auto px-5 lg:w-3/4">
              <WorkResultsOverview
                results={concept.works.slice(0, 3) as Work[]}
                totalResults={concept.works.length}
                heading="Related works"
                queryParams={{
                  subject: concept.id,
                }}
              />
            </div>
          )}
          {concept.stories.length > 0 && (
            <div className="mx-auto px-5 lg:w-3/4">
              <StoryResultsOverview
                queryParams={{
                  subject: concept.id,
                }}
                results={concept.stories.slice(0, 3) as Story[]}
                totalResults={concept.stories.length}
                heading="Related stories"
              />
            </div>
          )}
          {images.length > 0 && (
            <div className="mx-auto px-5 lg:w-3/4">
              <ImageResultsOverview
                heading="Related images"
                results={images.slice(0, 3)}
                totalResults={totalImages}
                queryParams={{
                  subject: concept.id,
                }}
              />
            </div>
          )}
        </div>
      </Layout>
    </div>
  )
}

export default SubjectPage
