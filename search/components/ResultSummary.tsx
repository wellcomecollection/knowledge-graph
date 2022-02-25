import { FC } from 'react'

type Props = {
  conceptId?: string
  index: string
  page: number
  personId?: string
  query?: string
  total: number
}
const ResultSummary: FC<Props> = ({
  conceptId,
  index,
  page,
  personId,
  query,
  total,
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
            )} of ${total} tagged with concept ID `}
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          </p>
        ) : (
          <p>
            {`${total} ${index} tagged with concept ID `}
            <a href={`/concepts/${conceptId}`}>{conceptId}</a>
          </p>
        )
      ) : personId ? (
        total > 10 ? (
          <p>
            <span className="capitalize">{index}</span>
            {` ${(page - 1) * 10 + 1}-${Math.min(
              page * 10,
              total
            )} of ${total} tagged with person ID `}
            <a href={`/people/${personId}`}>{personId}</a>
          </p>
        ) : (
          <p>
            {`${total} ${index} tagged with person ID `}
            <a href={`/people/${personId}`}>{personId}</a>
          </p>
        )
      ) : null}
    </>
  )
}

export default ResultSummary
