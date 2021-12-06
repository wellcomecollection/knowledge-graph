import {
  SourceConcept as ConceptType,
  StoryHit,
} from '../../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import IdTable from '../../components/IdTable'
import Layout from '../../components/Layout'
import StoryCard from '../../components/StoryCard'
import { getClient } from '../../services/elasticsearch'

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { id } = params as { id: string }
  const client = await getClient()
  const response = await client.get({
    index: process.env.ELASTIC_CONCEPTS_INDEX as string,
    id,
  })

  const fullStories = (await client
    .mget({
      index: process.env.ELASTIC_STORIES_INDEX as string,
      body: {
        ids: response.body._source.story_ids.split('<BREAK>').slice(0, 3),
      },
    })
    .then((res) => {
      return res.body.docs
    })) as StoryHit[]

  return { props: { ...response.body._source, fullStories, id } }
}
type Props = ConceptType & { fullStories: StoryHit[]; id: string }

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
            {props.variants.split('<BREAK>').map((variant) => (
              <li
                className="inline-block bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700 capitalize mr-2"
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
          {`We've written ${props.stories.split('<BREAK>').length} stories about
          this concept:`}
        </h2>

        <div className="pt-2 grid grid-cols-1 md:grid-cols-3 md:space-x-4 md:space-y-0 space-x-0 space-y-4 h-auto">
          {props.fullStories.map((story) => {
            const { _id, _source } = story
            const { standfirst, title } = _source
            return (
              <li className="inline-block" key={_id}>
                <StoryCard title={title} id={_id} standfirst={standfirst} />
              </li>
            )
          })}
        </div>
        <div className="pt-4">
          <a
            className="no-underline px-3 py-2 rounded border-2 border-black text-sm"
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
