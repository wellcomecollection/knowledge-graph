import { Concept, Person, Story } from '../types/elasticsearch'
import { GetServerSideProps, NextPage } from 'next'

import ConceptPanel from '../components/ConceptPanel'
import Layout from '../components/Layout'
import Paginator from '../components/Paginator'
import PersonPanel from '../components/PersonPanel'
import SearchBox from '../components/SearchBox'
import SearchResult from '../components/Hit'
import absoluteUrl from 'next-absolute-url'

type Props = {
  query: string
  conceptId: string
  personId: string
  total: number
  stories: Story[]
  concept: Concept | null
  person: Person | null
  page: number
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : ''
  const page = qs.page ? parseInt(qs.page.toString()) : 1
  const conceptId = qs.concept ? qs.concept.toString() : ''
  const personId = qs.person ? qs.person.toString() : ''

  let total: number = 0
  let stories: Story[] = []
  let concept: Concept | null = null
  let person: Person | null = null
  if (query || conceptId) {
    let url = new URL(`${absoluteUrl(req).origin}/api/search`)
    if (query) {
      url.searchParams.append('query', query)
    }
    if (conceptId) {
      url.searchParams.append('concept', conceptId)
    }
    if (personId) {
      url.searchParams.append('person', personId)
    }
    if (page) {
      url.searchParams.append('page', page.toString())
    }
    const response = await fetch(url.toString()).then((res) => res.json())
    total = response.stories.total
    stories = response.stories.results
    concept = response.concept.length > 0 ? response.concept[0] : null
    person = response.person.length > 0 ? response.person[0] : null
  }
  return {
    props: {
      query,
      conceptId,
      personId,
      person,
      total,
      stories,
      concept,
      page,
    },
  }
}

const Search: NextPage<Props> = ({
  query,
  conceptId,
  personId,
  total,
  stories,
  concept,
  person,
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
      {person ? <PersonPanel person={person} /> : null}
      <div className="pt-5">
        {query ? (
          `${total} results for "${query}"`
        ) : conceptId ? (
          <span>
            {total} results tagged with concept ID{' '}
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          </span>
        ) : personId ? (
          <span>
            {total} results tagged with person ID{' '}
            <a href={`/people/${personId}`}>{personId}</a>
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
      <Paginator
        page={page}
        total={total}
        query={query}
        conceptId={conceptId}
        personId={personId}
        stories={stories}
      />
    </Layout>
  )
}

export default Search
