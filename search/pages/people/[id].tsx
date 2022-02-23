import { GetServerSideProps, NextPage } from 'next'
import { Story, StoryHit } from '../../types/story'
import { Work, WorkHit } from '../../types/work'
import { getClient, parseStory, parseWork } from '../../services/elasticsearch'

import Card from '../../components/Card'
import { ConceptSource } from '../../types/concept'
import IdTable from '../../components/IdTable'
import Layout from '../../components/Layout'

type Props = ConceptSource & {
  fullWorks: Work[]
  fullStories: Story[]
  id: string
}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { id } = params as { id: string }
  const client = await getClient()
  const conceptsResponse = await client.get({
    index: process.env.ELASTIC_CONCEPTS_INDEX as string,
    id,
  })
  const work_contribution_ids =
    conceptsResponse.body._source.work_contribution_ids
  const story_contribution_ids =
    conceptsResponse.body._source.story_contribution_ids

  const fullWorks = (
    work_contribution_ids.length > 0
      ? await client
          .mget({
            index: process.env.ELASTIC_WORKS_INDEX as string,
            body: { ids: work_contribution_ids.slice(0, 3) },
          })
          .then((res) => {
            return res.body.docs
          })
      : []
  ).map((doc: WorkHit) => parseWork(doc))

  const fullStories = (
    story_contribution_ids.length > 0
      ? await client
          .mget({
            index: process.env.ELASTIC_STORIES_INDEX as string,
            body: { ids: story_contribution_ids.slice(0, 3) },
          })
          .then((res) => {
            return res.body.docs
          })
      : []
  ).map((doc: StoryHit) => parseStory(doc))

  return {
    props: {
      ...conceptsResponse.body._source,
      fullWorks,
      fullStories,
      id,
    },
  }
}

const Concept: NextPage<Props> = (props) => {
  const description = props.wikidata_description || props.mesh_description
  const title =
    props.wikidata_preferred_name ||
    props.mesh_preferred_name ||
    props.lc_subjects_preferred_name ||
    props.lc_names_preferred_name ||
    props.name

  return (
    <Layout title={`Concept | ${title}`} description={description}>
      <div className="space-y-6">
        <header>
          <h1>{title}</h1>
          <p>{description}</p>
        </header>
        <IdTable
          wikidata_id={props.wikidata_id}
          mesh_id={props.mesh_id}
          lc_subjects_id={props.lc_subjects_id}
          lc_names_id={props.lc_names_id}
        />
        {props.variants ? (
          <div>
            <h2 className="text-lg">Also known as</h2>
            <ul className="">
              {props.variants.map((variant) => (
                <li className="inline-block pr-1" key={variant}>
                  <span className="bg-paper-3 px-2 py-1 text-xs capitalize">
                    {variant}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
        {props.story_contribution_ids.length > 0 ? (
          <div>
            <h2 className="text-lg font-bold">
              {`We've got ${props.story_contribution_ids.length} stories by this person:`}
            </h2>
            <div className="grid h-auto grid-cols-1 space-x-0 space-y-2 pt-2 md:grid-cols-3 md:space-x-2 md:space-y-0">
              {props.fullStories.map((story: Story) => {
                const { id, contributors, type, title } = story
                return (
                  <li className="inline-block" key={id}>
                    <Card
                      id={id}
                      color={type === 'work' ? 'blue' : 'green'}
                      contributors={contributors.map(
                        (contributor) => contributor.name
                      )}
                      type={type}
                      title={title}
                    />
                  </li>
                )
              })}
            </div>
            <div className="pt-2">
              <a
                className="bg-green px-3 py-2 text-sm no-underline"
                href={`/?concept=${props.id}`}
              >
                See more →
              </a>
            </div>
          </div>
        ) : null}
        {props.work_contribution_ids.length > 0 ? (
          <div>
            <h2 className="text-lg font-bold">
              {`We've got ${props.work_contribution_ids.length} works by this person:`}
            </h2>

            <div className="grid h-auto grid-cols-1 space-x-0 space-y-2 pt-2 md:grid-cols-3 md:space-x-2 md:space-y-0">
              {props.fullWorks.map((work: Work) => {
                const { id, contributors, type, title } = work
                return (
                  <li className="inline-block" key={id}>
                    <Card
                      id={id}
                      color={type === 'work' ? 'pink' : 'green'}
                      contributors={contributors.map(
                        (contributor) => contributor.name
                      )}
                      type={type}
                      title={title}
                    />
                  </li>
                )
              })}
            </div>
            <div className="pt-2">
              <a
                className="bg-pink px-3 py-2 text-sm no-underline"
                href={`/?concept=${props.id}`}
              >
                See more →
              </a>
            </div>
          </div>
        ) : null}
      </div>
    </Layout>
  )
}

export default Concept
