import { GetServerSideProps, NextPage } from 'next'
import { Image, ImageSource } from '../../types/image'
import { getClient, getPerson } from '../../services/elasticsearch'

import { ArrowUpRight } from 'react-feather'
import Head from 'next/head'
import ImageResultsOverview from '../../components/results/overview/images'
import Layout from '../../components/layout'
import { Person } from '../../types/person'
import { Story } from '../../types/story'
import StoryResultsOverview from '../../components/results/overview/stories'
import { Work } from '../../types/work'
import WorkResultsOverview from '../../components/results/overview/works'
import { capitalise } from '../../components/results'

type Props = {
  person: Person
  images: Image[]
  totalImages: number
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const personId = query.id as string
  const client = getClient()
  const person = await getPerson(client, personId)
  const capitalisedPersonName = capitalise(person.label)
  const url = `https://api.wellcomecollection.org/catalogue/v2/images?source.subjects.label=${capitalisedPersonName}`
  const imageResponse = await fetch(url).then((res) => res.json())
  const images = imageResponse.results.map((image: ImageSource) => {
    return {
      id: image.source.id,
      url: image.thumbnail.url.replace('info.json', 'full/400,/0/default.jpg'),
      title: image.source.title,
    }
  })
  const totalImages = imageResponse.totalResults
  return { props: { person, images, totalImages } }
}

const PersonPage: NextPage<Props> = ({ person, images, totalImages }) => {
  const description =
    person.wikidata_description || person.mesh_description || null
  const capitalisedDescription = description
    ? description?.charAt(0).toUpperCase() + description?.slice(1)
    : null
  return (
    <div className="">
      <Head>
        <title>{person.preferred_label}</title>
      </Head>
      <Layout>
        <div className="space-y-8 bg-red py-8">
          <div className="mx-auto  px-5 lg:w-3/4">
            <h1 className="font-sans text-5xl capitalize">
              {person.preferred_label}
            </h1>
          </div>
          <div className="mx-auto flex flex-col space-y-8 px-5 lg:w-3/4 lg:flex-row lg:space-y-0 lg:space-x-12">
            <div className="space-y-4 lg:w-2/3">
              <p className="font-sans text-lg">{capitalisedDescription}</p>
              <div className="flex flex-col ">
                {person.wikidata_id && (
                  <a
                    href={`https://www.wikidata.org/wiki/${person.wikidata_id}`}
                  >
                    Read more on Wikidata <ArrowUpRight className="inline" />
                  </a>
                )}
                {person.mesh_id && (
                  <a href={`https://id.nlm.nih.gov/mesh/${person.mesh_id}`}>
                    Read more on MeSH <ArrowUpRight className="inline" />
                  </a>
                )}
                {person.lc_subjects_id && (
                  <a
                    href={`https://id.loc.gov/authorities/subjects/${person.lc_subjects_id}`}
                  >
                    Read more on Library of Congress (subjects)
                    <ArrowUpRight className="inline" />
                  </a>
                )}
                {person.lc_names_id && (
                  <a
                    href={`https://id.loc.gov/authorities/names/${person.lc_names_id}`}
                  >
                    Read more on Library of Congress (names)
                    <ArrowUpRight className="inline" />
                  </a>
                )}
              </div>
              <div>
                <p className="font-bold">Also known as</p>
                <p>
                  {person.variants
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
              <p className="font-bold">Related people</p>
              <ul className="flex flex-wrap gap-x-2 pt-4 ">
                {person.neighbours.map((neighbour) => (
                  <li key={neighbour.id} className="pb-6">
                    <a
                      className="w-100 rounded-full border border-black py-2 px-3 text-sm capitalize no-underline"
                      href={`/people/${neighbour.id}`}
                    >
                      {neighbour.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        {person.work_contributions.length > 0 && (
          <div className="mx-auto px-5 lg:w-3/4">
            <WorkResultsOverview
              results={person.work_contributions.slice(0, 3) as Work[]}
              totalResults={person.work_contributions.length}
              heading="Works by this person"
              queryParams={{
                person: person.id,
              }}
            />
          </div>
        )}
        {person.works.length > 0 && (
          <div className="mx-auto px-5 lg:w-3/4">
            <WorkResultsOverview
              results={person.works.slice(0, 3) as Work[]}
              totalResults={person.works.length}
              heading="Works about this person"
              queryParams={{
                person: person.id,
              }}
            />
          </div>
        )}
        {person.story_contributions.length > 0 && (
          <div className="mx-auto px-5 lg:w-3/4">
            <StoryResultsOverview
              queryParams={{
                person: person.id,
              }}
              results={person.story_contributions.slice(0, 3) as Story[]}
              totalResults={person.story_contributions.length}
              heading="Stories by this person"
            />
          </div>
        )}
        {person.stories.length > 0 && (
          <div className="mx-auto px-5 lg:w-3/4">
            <StoryResultsOverview
              queryParams={{
                person: person.id,
              }}
              results={person.stories.slice(0, 3) as Story[]}
              totalResults={person.stories.length}
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
                person: person.id,
              }}
            />
          </div>
        )}
      </Layout>
    </div>
  )
}

export default PersonPage
