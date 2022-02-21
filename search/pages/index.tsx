import { GetServerSideProps, NextPage } from 'next'

import { Concept } from '../types/concept'
import ConceptPanel from '../components/ConceptPanel'
import Layout from '../components/Layout'
import Paginator from '../components/Paginator'
import SearchBox from '../components/SearchBox'
import SearchResult from '../components/Hit'
import { Work } from '../types/work'
import absoluteUrl from 'next-absolute-url'

type Props = {
  query: string
  conceptId: string
  personId: string
  total: number
  works: Work[]
  concept: Concept | null
  person: Concept | null
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
  let works: Work[] = []
  let concept: Concept | null = null
  let person: Concept | null = null
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
    total = response.works.total
    works = response.works.results
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
      works,
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
  works,
  concept,
  person,
  page,
}) => {
  return (
    <Layout
      title="Knowledge-graph search"
      description="Search for works, stories, and concepts in Wellcome Collection"
    >
      <h1>Knowledge-graph search</h1>
      <p>
        Search for works, stories, and concepts from{' '}
        <a href="https://wellcomecollection.org/">Wellcome Collection</a>.
      </p>
      <div className="pt-4">
        <SearchBox query={query} />
      </div>
      {concept ? <ConceptPanel concept={concept} color={'green'} /> : null}
      {person ? <ConceptPanel concept={person} color={'blue'} /> : null}
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
      <ul className="space-y-5 divide-y divide">
        {works.map((work) => (
          <li key={work.id} className="pt-4">
            <SearchResult work={work} />
          </li>
        ))}
      </ul>
      <Paginator
        page={page}
        total={total}
        query={query}
        conceptId={conceptId}
        personId={personId}
        works={works}
      />
    </Layout>
  )
}

export default Search
