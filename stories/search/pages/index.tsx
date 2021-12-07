import { Concept, Story } from '../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import ConceptPanel from '../components/Panel'
import Layout from '../components/Layout'
import SearchBox from '../components/SearchBox'
import SearchResult from '../components/Hit'
import absoluteUrl from 'next-absolute-url'

type Props = {
  query: string
  conceptId: string
  total: number
  stories: Story[]
  concept: Concept | null
  page: number
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : ''
  const page = qs.page ? parseInt(qs.page.toString()) : 1
  const conceptId = qs.concept ? qs.concept.toString() : ''

  let total: number = 0
  let stories: Story[] = []
  let concept: Concept | null = null
  if (query || conceptId) {
    let url = new URL(`${absoluteUrl(req).origin}/api/search`)
    if (query) {
      url.searchParams.append('query', query)
    }
    if (conceptId) {
      url.searchParams.append('concept', conceptId)
    }
    if (page) {
      url.searchParams.append('page', page.toString())
    }
    const response = await fetch(url.toString()).then((res) => res.json())
    total = response.stories.total
    stories = response.stories.results
    concept = response.concept.length > 0 ? response.concept[0] : null
  }
  return {
    props: { query, conceptId, total, stories, concept, page },
  }
}

const Search: NextPage<Props> = ({
  query,
  conceptId,
  total,
  stories,
  concept,
  page,
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
      {concept ? <ConceptPanel concept={concept} /> : null}
      <div className="pt-5">
        {query ? (
          `${total} results for "${query}"`
        ) : conceptId ? (
          <span>
            {total} results tagged with concept ID{' '}
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          </span>
        ) : null}
      </div>
      <ul className="space-y-5 divide-y divide-gray-400">
        {stories.map((story) => (
          <li key={story.id} className="pt-4">
            <SearchResult story={story} />
          </li>
        ))}
      </ul>
      {total > 10 ? (
        <div className="pt-7 space-x-4">
          {page > 1 ? (
            <a
              className="no-underline px-3 py-2 rounded border-2 border-black"
              href={`/${query ? `?query=${query}` : ''}${
                conceptId ? `?concept=${conceptId}` : ''
              }&page=${page - 1}`}
            >
              ← previous
            </a>
          ) : null}
          <span>Page {page}</span>
          {!(stories.length < 10) ? (
            <a
              className="no-underline px-3 py-2 rounded border-2 border-black "
              href={`/${query ? `?query=${query}` : ''}${
                conceptId ? `?concept=${conceptId}` : ''
              }&page=${page ? page + 1 : 2}`}
            >
              next →
            </a>
          ) : null}
        </div>
      ) : null}
    </Layout>
  )
}

export default Search
