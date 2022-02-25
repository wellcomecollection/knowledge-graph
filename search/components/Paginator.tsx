import { FC } from 'react'

type Props = {
  conceptId: string
  index: string
  length: number
  page: number
  personId: string
  query: string
  total: number
}

const Paginator: FC<Props> = ({
  conceptId,
  index,
  length,
  page,
  personId,
  query,
  total,
}) => {
  const params = new URLSearchParams({
    concept: conceptId,
    index,
    person: personId,
    query,
  })
  const url = `/?${params.toString()}`

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
