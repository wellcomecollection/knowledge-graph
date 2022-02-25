import { GetServerSideProps, NextPage } from 'next'

import { Concept } from '../types/concept'
import ConceptPanel from '../components/ConceptPanel'
import Layout from '../components/Layout'
import Paginator from '../components/Paginator'
import ResultSummary from '../components/ResultSummary'
import SearchBox from '../components/SearchBox'
import SearchResult from '../components/SearchResult'
import { Story } from '../types/story'
import { Work } from '../types/work'
import absoluteUrl from 'next-absolute-url'

type Props = {
  query: string
  index: string
  conceptId: string
  personId: string
  total: number
  results: Work[] | Story[]
  concept: Concept | null
  person: Concept | null
  page: number
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  // parse the query string
  const index = qs.index ? qs.index.toString() : 'works'
  const query = qs.query ? qs.query.toString() : ''
  const page = qs.page ? parseInt(qs.page.toString()) : 1
  const conceptId = qs.concept ? qs.concept.toString() : ''
  const personId = qs.person ? qs.person.toString() : ''

  // get the results from the API
  let total: number = 0
  let results: Work[] | Story[] = []
  let concept: Concept | null = null
  let person: Concept | null = null
  if ((query && index) || conceptId || personId) {
    let url = new URL(`${absoluteUrl(req).origin}/api/search/${index}`)
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

    total = response.total
    results = response.results
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
      results,
      concept,
      page,
      index,
    },
  }
}

const Search: NextPage<Props> = ({
  query,
  conceptId,
  personId,
  total,
  results,
  concept,
  person,
  page,
  index,
}) => {
  const title = 'Knowledge-graph search'
  const description =
    'Search for works, stories, and concepts from Wellcome Collection.'
  return (
    <Layout title={title} description={description}>
      <div className="space-y-5">
        <header>
          <h1>{title}</h1>
          <p>{description}</p>
        </header>

        <SearchBox query={query} index={index} />

        {query && concept ? (
          <ConceptPanel concept={concept} />
        ) : null}
        {query && person ? (
          <ConceptPanel concept={person} />
        ) : null}

        <div>
          <ResultSummary
            query={query}
            index={index}
            total={total}
            page={page}
            conceptId={conceptId}
            personId={personId}
          />

          <ul className="divide-y divide-green ">
            {results.map((result) => (
              <li key={result.id} className="py-4 ">
                <SearchResult result={result} />
              </li>
            ))}
          </ul>
        </div>

        <Paginator
          page={page}
          total={total}
          query={query}
          conceptId={conceptId}
          personId={personId}
          length={results.length}
          index={index}
        />
      </div>
    </Layout>
  )
}

export default Search
