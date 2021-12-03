import { ConceptHit, StoryHit } from '../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import ConceptPanel from '../components/Panel'
import Hit from '../components/Hit'
import Layout from '../components/Layout'
import SearchBox from '../components/SearchBox'
import absoluteUrl from 'next-absolute-url'

type Props = {
  storyHits: StoryHit[]
  query: string
  conceptFilter: string
  total: number
  conceptHits: ConceptHit[]
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const { origin } = absoluteUrl(req)
  const query = qs.query ? qs.query.toString() : ''
  const conceptFilter = qs.concept ? qs.concept.toString() : ''

  let total = 0
  let storyHits: StoryHit[] = []
  let conceptHits: ConceptHit[] = []
  if (query) {
    const encodedQuery = encodeURIComponent(query)
    const storiesResponse = await fetch(
      `${origin}/api/stories?q=${encodedQuery}`
    ).then((res) => res.json())
    const conceptsResponse = await fetch(
      `${origin}/api/concepts?q=${encodedQuery}`
    ).then((res) => res.json())

    storyHits = storiesResponse.hits
    total = storiesResponse.total.value
    conceptHits = conceptsResponse.hits
  } else if (conceptFilter) {
    const storiesResponse = await fetch(
      `${origin}/api/stories?concept=${conceptFilter}`
    ).then((res) => res.json())
    storyHits = storiesResponse.hits
    total = storiesResponse.total.value
  }
  return {
    props: { query, total, storyHits, conceptHits, conceptFilter },
  }
}

const Search: NextPage<Props> = ({
  storyHits,
  query,
  total,
  conceptHits,
  conceptFilter,
}) => {
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
      {conceptHits.length > 0 ? (
        <ConceptPanel conceptHit={conceptHits[0]} />
      ) : null}
      {storyHits.length > 0 ? (
        <div className="py-5">
          {query ? <p>{`${total} results for "${query}"`}</p> : null}
          {conceptFilter ? (
            <p>
              {total} results for concept ID {conceptFilter}
            </p>
          ) : null}
          <ul className="space-y-5 divide-y divide-gray-400">
            {storyHits.map((hit) => (
              <li key={hit._id} className="pt-4">
                <Hit hit={hit} />
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </Layout>
  )
}

export default Search
