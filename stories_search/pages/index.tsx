import { GetServerSideProps, NextPage } from 'next'

import Hit from '../components/Hit'
import { Hit as HitType } from '../types/elasticsearch'
import SearchBox from '../components/SearchBox'
import absoluteUrl from 'next-absolute-url'

type Props = {
  hits: HitType[]
  query?: string
}

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  const query = qs.query ? qs.query.toString() : ''

  let hits: HitType[] = []
  if (query) {
    const { origin } = absoluteUrl(req)
    const url = `${origin}/api/search?q=${encodeURIComponent(query)}`
    const data = await fetch(url).then((res) => res.json())
    hits = data.hits ? data.hits : []
  }

  return {
    props: { hits, query },
  }
}

const Search: NextPage<Props> = ({ hits, query }) => {
  return (
    <>
      <h1>Stories search</h1>
      <div>
        Search for stories on{' '}
        <a href="https://wellcomecollection.org/stories">
          wellcomecollection.org/stories
        </a>
      </div>
      <SearchBox query={query} />
      <ul>
        {hits.map((hit) => (
          <li key={hit._id}>
            <Hit hit={hit} />
          </li>
        ))}
      </ul>
    </>
  )
}

export default Search
