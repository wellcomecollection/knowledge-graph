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
    <div className="pt-7 space-x-4">
      {page > 1 ? (
        <a
          className="no-underline px-3 py-2 rounded border-2 border-black"
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
          className="no-underline px-3 py-2 rounded border-2 border-black"
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
