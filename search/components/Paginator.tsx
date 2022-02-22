import { FC } from 'react'

type Props = {
  total: number
  page: number
  query: string
  conceptId?: string
  personId?: string
  length: number
  index: string
}

const Paginator: FC<Props> = ({
  total,
  index,
  page,
  query,
  conceptId,
  personId,
  length,
}) => {
  const url = `/?query=${query}&index=${index}`
  if (conceptId) {
    url + `&concept=${conceptId}`
  }
  if (personId) {
    url + `&person=${personId}`
  }

  return total > 10 ? (
    <div>
      {page > 1 ? (
        <a
          className="bg-paper-2 px-3 py-2 no-underline"
          href={url + `&page=${page - 1}`}
        >
          ← previous
        </a>
      ) : null}
      <span className="bg-paper-3 px-3 py-2">Page {page}</span>
      {!(length < 10) ? (
        <a
          className="bg-paper-2 px-3 py-2 no-underline"
          href={url + `&page=${page + 1}`}
        >
          next →
        </a>
      ) : null}
    </div>
  ) : null
}
export default Paginator
