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

  const workIDs = conceptsResponse.body._source.work_ids
  const storyIDs = conceptsResponse.body._source.story_ids

  const fullWorks = (
    workIDs.length > 0
      ? await client
          .mget({
            index: process.env.ELASTIC_WORKS_INDEX as string,
            body: { ids: workIDs },
          })
          .then((res) => {
            return res.body.docs
          })
          .then((docs) => {
            docs.map((doc: WorkHit) => parseWork(doc))
          })
      : []
  ) as Work[]

  const fullStories = (
    storyIDs.length > 0
      ? await client
          .mget({
            index: process.env.ELASTIC_STORIES_INDEX as string,
            body: { ids: storyIDs },
          })
          .then((res) => {
            return res.body.docs
          })
          .then((docs) => {
            docs.map((doc: StoryHit) => parseStory(doc))
          })
      : []
  ) as Story[]

  return {
    props: { ...conceptsResponse.body._source, fullWorks, fullStories, id },
  }
}

const Concept: NextPage<Props> = (props) => {
  const description = props.wikidata_description || props.mesh_description
  const title =
    props.wikidata_preferred_name ||
    props.mesh_preferred_name ||
    props.lcsh_preferred_name ||
    props.name

  return (
    <Layout title={title} description={description}>
      <h1>{title}</h1>
      <p>{description}</p>
      <IdTable
        wikidata_id={props.wikidata_id}
        mesh_id={props.mesh_id}
        lcsh_id={props.lcsh_id}
      />
      {props.variants ? (
        <div className="pt-4">
          <h2 className="text-lg">Also known as</h2>
          <ul>
            {props.variants.map((variant) => (
              <li
                className="mr-2 inline-block rounded-lg bg-gray-200 px-2 py-1 text-xs capitalize text-gray-700"
                key={variant}
              >
                {variant}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      <div className="pt-4">
        <h2 className="text-lg font-bold">
          {`We've got ${props.fullStories.length} stories about
          this concept:`}
        </h2>

        <div className="grid h-auto grid-cols-1 space-x-0 space-y-4 pt-2 md:grid-cols-3 md:space-x-4 md:space-y-0">
          {props.fullStories.map((story: Story) => {
            const { id, standfirst, type, title } = story
            return (
              <li className="inline-block" key={id}>
                <Card
                  id={id}
                  description={standfirst}
                  type={type}
                  title={title}
                />
              </li>
            )
          })}
        </div>
        <div className="pt-4">
          <a
            className="rounded border-2 border-black px-3 py-2 text-sm no-underline"
            href={`/?concept=${props.id}`}
          >
            See more →
          </a>
        </div>
      </div>

      <div className="pt-4">
        <h2 className="text-lg font-bold">
          {`We've got ${props.fullWorks.length} works about
          this concept:`}
        </h2>

        <div className="grid h-auto grid-cols-1 space-x-0 space-y-4 pt-2 md:grid-cols-3 md:space-x-4 md:space-y-0">
          {props.fullWorks.map((work: Work) => {
            const { id, description, type, title } = work
            return (
              <li className="inline-block" key={id}>
                <Card
                  title={title}
                  id={id}
                  description={description}
                  type={type}
                />
              </li>
            )
          })}
        </div>
        <div className="pt-4">
          <a
            className="rounded border-2 border-black px-3 py-2 text-sm no-underline"
            href={`/?concept=${props.id}`}
          >
            See more →
          </a>
        </div>
      </div>
    </Layout>
  )
}

export default Concept
