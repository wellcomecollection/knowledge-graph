import { FC } from 'react'
import { Story } from '../types/elasticsearch'

type Props = {
  total: number
  page: number
  query: string
  conceptId: string
  personId: string
  stories: Story[]
}
const Paginator: FC<Props> = ({
  total,
  page,
  query,
  conceptId,
  personId,
  stories,
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
      {!(stories.length < 10) ? (
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
