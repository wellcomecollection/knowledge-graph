import {
  SourceConcept as ConceptType,
  StoryHit,
} from '../../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import Layout from '../../components/Layout'
import StoryCard from '../../components/WorkCard'
import { getClient } from '../../services/elasticsearch'

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { id } = params as { id: string }
  const client = await getClient()
  const response = await client.get({
    index: process.env.ELASTIC_PEOPLE_INDEX as string,
    id,
  })

  const fullStories = (await client
    .mget({
      index: process.env.ELASTIC_STORIES_INDEX as string,
      body: {
        ids: response.body._source.story_ids.slice(0, 3),
      },
    })
    .then((res) => {
      return res.body.docs
    })) as StoryHit[]

  return { props: { ...response.body._source, fullStories, id } }
}
type Props = ConceptType & { fullStories: StoryHit[]; id: string }

const Concept: NextPage<Props> = (props) => {
  const description = props.wikidata_description
  const title = props.wikidata_preferred_name || props.name
  return (
    <Layout title={title} description={description}>
      <h1 className="capitalize">{title}</h1>
      <p>{description}</p>
      <div className="pt-4">
        <h2 className="text-lg font-bold">
          <span className="capitalize">{title}</span> has written{' '}
          {props.stories.length} stories for Wellcome Collection:
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
            href={`/?person=${props.id}`}
          >
            See more →
          </a>
        </div>
      </div>
    </Layout>
  )
}

export default Concept
