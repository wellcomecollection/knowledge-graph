import { FC } from 'react'
import { Work } from '../types/work'

type Props = {
  total: number
  page: number
  query: string
  conceptId: string
  personId: string
  works: Work[]
}
const Paginator: FC<Props> = ({
  total,
  page,
  query,
  conceptId,
  personId,
  works,
}) => {
  return total > 10 ? (
    <div className="space-x-4 pt-7">
      {page > 1 ? (
        <a
          className="rounded border-2 border-black px-3 py-2 no-underline"
          href={`/${query ? `?query=${query}` : ''}${
            conceptId ? `?concept=${conceptId}` : ''
          }${personId ? `?person=${personId}` : ''}&page=${page - 1}`}
        >
          ← previous
        </a>
      ) : null}
      <span>Page {page}</span>
      {!(works.length < 10) ? (
        <a
          className="rounded border-2 border-black px-3 py-2 no-underline"
          href={`/${query ? `?query=${query}` : ''}${
            conceptId ? `?concept=${conceptId}` : ''
          }${personId ? `?person=${personId}` : ''}&page=${
            page ? page + 1 : 2
          }`}
        >
          next →
        </a>
      ) : null}
    </div>
  ) : null
}
export default Paginator
