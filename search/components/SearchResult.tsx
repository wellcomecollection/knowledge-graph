import { FC } from 'react'
import Link from 'next/link'
import { Story } from '../types/story'
import { Work } from '../types/work'

type Props = { result: Work | Story }
const SearchResult: FC<Props> = ({ result }) => {
  const contributors =
    result.contributors.length > 0
      ? result.contributors
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
        href={`https://wellcomecollection.org/${
          result.type === 'work' ? 'works' : 'articles'
        }/${result.id}`}
        className="no-underline"
      >
        <h3 className="text-xl">{result.title}</h3>
        <div className="text-sm capitalize">{contributors}</div>
      </a>
      <ul className="pt-2 leading-7">
        {result.concepts.map((concept) => (
          <li key={concept.id} className="inline-block pr-1">
            <Link href={`/concepts/${concept.id}`}>
              <a className="bg-paper-2 px-2 py-1 text-xs no-underline">
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
