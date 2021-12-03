import { GetServerSideProps, NextPage } from 'next'

import Hit from '../components/Hit'
import { Hit as HitType } from '../types/elasticsearch'
import Layout from '../components/Layout'
import SearchBox from '../components/SearchBox'
import absoluteUrl from 'next-absolute-url'

type Props = {
  hits: HitType[]
  query?: string
  total: number
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : ''

  let hits: HitType[] = []
  let total = 0
  if (query) {
    const { origin } = absoluteUrl(req)
    const url = `${origin}/api/search?q=${encodeURIComponent(query)}`
    const data = await fetch(url).then((res) => res.json())
    hits = data.hits ? data.hits : []
    total = data.total.value
  }

  return {
    props: { hits, query, total },
  }
}

const Search: NextPage<Props> = ({ hits, query, total }) => {
  return (
    <Layout
      title="Stories search"
      description="Search for stories on wellcomecollection.org/stories"
    >
      <div className="py-2">
        <h1>Stories search</h1>
        <p>
          Search for stories on{' '}
          <a href="https://wellcomecollection.org/stories">
            wellcomecollection.org/stories
          </a>
        </p>
      </div>
      <div className="py-4">
        <SearchBox query={query} />
      </div>
      {hits.length > 0 ? (
        <div>
          <p>
            {total} results for "{query}"
          </p>
          <ul className="divide-y divide-gray-500">
            {hits.map((hit) => (
              <li key={hit._id} className="py-4">
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
