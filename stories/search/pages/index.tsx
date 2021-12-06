import { Concept, ConceptHit, Story, StoryHit } from '../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import ConceptPanel from '../components/Panel'
import Layout from '../components/Layout'
import SearchBox from '../components/SearchBox'
import SearchResult from '../components/Hit'
import absoluteUrl from 'next-absolute-url'

type Props = {
  query: string
  conceptId: string
  stories: Story[]
  concept: Concept
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const { origin } = absoluteUrl(req)
  const query = qs.query ? qs.query.toString() : ''
  const conceptId = qs.concept ? qs.concept.toString() : ''

  let stories: StoryHit[] = []
  let concept: ConceptHit | null = null
  if (query || conceptId) {
    var url = new URL(`${origin}/api/search`)
    url.search = new URLSearchParams({
      query: encodeURIComponent(query),
      concept: conceptId ? conceptId : '',
    }).toString()

    const response = await fetch(url.toString()).then((res) => res.json())
    stories = response.stories
    concept = response.concept.length > 0 ? response.concept[0] : null
  }
  return {
    props: { query, conceptId, stories, concept },
  }
}

const Search: NextPage<Props> = ({ query, conceptId, stories, concept }) => {
  return (
    <Layout
      title="Stories search"
      description="Search for stories on wellcomecollection.org/stories"
    >
      <h1>Stories search</h1>
      <p>
        Search for stories on{' '}
        <a href="https://wellcomecollection.org/stories">
          wellcomecollection.org/stories
        </a>
      </p>
      <div className="pt-4">
        <SearchBox query={query} />
      </div>
      {concept ? <ConceptPanel concept={concept} /> : null}
      {stories.length > 0 ? (
        <div className="py-5">
          {query ? <p>{`${stories.length} results for "${query}"`}</p> : null}
          {conceptId ? (
            <p>
              {stories.length} results tagged with concept ID{' '}
              <a href={`/concepts/${conceptId}`}>{conceptId}</a>
            </p>
          ) : null}
          <ul className="space-y-5 divide-y divide-gray-400">
            {stories.map((story) => (
              <li key={story.id} className="pt-4">
                <SearchResult story={story} />
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </Layout>
  )
}

export default Search
