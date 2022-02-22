import { FC } from 'react'

type Props = {
  query?: string
  index: string
  total: number
  page: number
  conceptId?: string
  personId?: string
}
const ResultSummary: FC<Props> = ({
  query,
  index,
  total,
  page,
  conceptId,
  personId,
}) => {
  return (
    <>
      {query ? (
        total > 10 ? (
          <p>
            <span className="capitalize">{index}</span>
            {` ${(page - 1) * 10 + 1}-${Math.min(
              page * 10,
              total
            )} of ${total} matching "${query}"`}
          </p>
        ) : (
          <p>{`${total} ${index} matching "${query}"`}</p>
        )
      ) : conceptId ? (
        total > 10 ? (
          <p>
            <span className="capitalize">{index}</span>
            {` ${(page - 1) * 10 + 1}-${Math.min(
              page * 10,
              total
            )} of ${total} tagged with`}
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          </p>
        ) : (
          <p>{`${total} ${index} tagged with ${(
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          )}`}</p>
        )
      ) : personId ? (
        <span>
          {total} results tagged with person ID{' '}
          <a href={`/people/${personId}`}>{personId}</a>
        </span>
      ) : null}
    </>
  )
}

export default ResultSummary
