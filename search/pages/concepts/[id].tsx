import { GetServerSideProps, NextPage } from 'next'
import { getClient, getSubject } from '../../services/elasticsearch'

import { ArrowUpRight } from 'react-feather'
import { Concept } from '../../types/concept'
import Head from 'next/head'
import Layout from '../../components/layout'

type Props = {
  concept: Concept
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const conceptId = query.id as string
  const client = getClient()
  const concept = await getSubject(client, conceptId)
  return { props: { concept } }
}

const ConceptPage: NextPage<Props> = ({ concept }) => {
  const description =
    concept.wikidata_description || concept.mesh_description || null
  const capitalisedDescription = description
    ? description?.charAt(0).toUpperCase() + description?.slice(1)
    : null
  return (
    <div className="">
      <Head>
        <title>{concept.name}</title>
      </Head>
      <Layout>
        <div className="space-y-8 bg-red py-8">
          <div className="mx-auto  px-5 lg:w-3/4">
            <h1 className="font-sans text-5xl capitalize">{concept.name}</h1>
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
                      href={`/concepts/${neighbour.id}`}
                    >
                      {neighbour.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className="mx-auto space-y-8 px-5 lg:w-3/4">
          <h2 className="font-sans font-light">Related works</h2>
          {concept.works.map((work: { id: string; name: string }) => (
            <div className="flex flex-col space-y-2" key={work.id}>
              <a href={`/work/${work.id}`}>
                <h3 className="font-sans font-light">{work.name}</h3>
              </a>
            </div>
          ))}
        </div>
      </Layout>
    </div>
  )
}

export default ConceptPage
