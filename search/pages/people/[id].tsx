import { GetServerSideProps, NextPage } from 'next'
import { getClient, getPerson } from '../../services/elasticsearch'

import { ArrowUpRight } from 'react-feather'
import Head from 'next/head'
import Layout from '../../components/layout'
import { Person } from '../../types/person'

type Props = {
  person: Person
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const personId = query.id as string
  const client = getClient()
  const person = await getPerson(client, personId)
  return { props: { person } }
}

const PersonPage: NextPage<Props> = ({ person }) => {
  const description =
    person.wikidata_description || person.mesh_description || null
  const capitalisedDescription = description
    ? description?.charAt(0).toUpperCase() + description?.slice(1)
    : null
  return (
    <div className="">
      <Head>
        <title>{person.preferred_name}</title>
      </Head>
      <Layout>
        <div className="space-y-8 bg-red py-8">
          <div className="mx-auto  px-5 lg:w-3/4">
            <h1 className="font-sans text-5xl capitalize">
              {person.preferred_name}
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
                      {neighbour.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        {person.works.length > 0 && (
          <div className="mx-auto space-y-4 px-5 lg:w-3/4">
            <h2 className="font-sans font-light">Works about this person</h2>
            <div className="flex flex-col space-y-2">
              {person.works.map((work: { id: string; name: string }) => (
                <a href={`/works/${work.id}`} key={work.id}>
                  <h3 className="font-sans font-light">{work.name}</h3>
                </a>
              ))}
            </div>
          </div>
        )}
        {person.work_contributions.length > 0 && (
          <div className="mx-auto space-y-4 px-5 lg:w-3/4">
            <h2 className="font-sans font-light">Works by this person</h2>
            <div className="flex flex-col space-y-2">
              {person.work_contributions.map(
                (work: { id: string; name: string }) => (
                  <a href={`/works/${work.id}`} key={work.id}>
                    <h3 className="font-sans font-light">{work.name}</h3>
                  </a>
                )
              )}
            </div>
          </div>
        )}
        {person.stories.length > 0 && (
          <div className="mx-auto space-y-4 px-5 lg:w-3/4">
            <h2 className="font-sans font-light">Stories about this person</h2>
            <div className="flex flex-col space-y-2">
              {person.stories.map((story: { id: string; name: string }) => (
                <a
                  href={`https://wellcomecollection.org/articles/${story.id}`}
                  key={story.id}
                >
                  <h3 className="font-sans font-light">{story.name}</h3>
                </a>
              ))}
            </div>
          </div>
        )}
        {person.story_contributions.length > 0 && (
          <div className="mx-auto space-y-4 px-5 lg:w-3/4">
            <h2 className="font-sans font-light">Stories by this person</h2>
            <div className="flex flex-col space-y-2">
              {person.story_contributions.map(
                (story: { id: string; name: string }) => (
                  <a
                    href={`https://wellcomecollection.org/articles/${story.id}`}
                    key={story.id}
                  >
                    <h3 className="font-sans font-light">{story.name}</h3>
                  </a>
                )
              )}
            </div>
          </div>
        )}
        {person.stories.length > 0 && (
          <div className="mx-auto space-y-4 px-5 lg:w-3/4">
            <h2 className="font-sans font-light">Related stories</h2>
            <div className="flex flex-col space-y-2">
              {person.stories.map((story: { id: string; name: string }) => (
                <a
                  key={story.id}
                  href={`https://wellcomecollection.org/articles/${story.id}`}
                >
                  <h3 className="font-sans font-light">{story.name}</h3>
                </a>
              ))}
            </div>
          </div>
        )}
      </Layout>
    </div>
  )
}

export default PersonPage
