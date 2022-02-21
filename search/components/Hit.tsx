import { FC } from 'react'
import Link from 'next/link'
import { Work } from '../types/work'

type Props = { work: Work }
const SearchResult: FC<Props> = ({ work }) => {
  const contributors =
    work.contributors.length > 0
      ? work.contributors
          .map<React.ReactNode>((contributor) => {
            return (
              <span key={contributor.id}>
                <a className="no-underline" href={`/people/${contributor.id}`}>
                  {contributor.name}
                </a>
              </span>
            )
          })
          .reduce((acc, curr) => [acc, ', ', curr])
      : null

  return (
    <>
      <a
        href={`https://wellcomecollection.org/works/${work.id}`}
        className="no-underline"
      >
        <p className="text-xl font-bold">{work.title}</p>
        <div className="text-sm capitalize">{contributors}</div>
      </a>
      <ul className="pt-2 leading-7">
        {work.concepts.map((concept) => (
          <li key={concept.id} className="inline-block pr-2">
            <Link href={`/concepts/${concept.id}`}>
              <a className="rounded-lg bg-paper-2 px-2 py-1 text-xs no-underline">
                {concept.name}
              </a>
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export default SearchResult
