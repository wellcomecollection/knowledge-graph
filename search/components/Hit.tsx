import { FC } from 'react'
import Link from 'next/link'
import { Work } from '../types/elasticsearch'

type Props = { work: Work }
const SearchResult: FC<Props> = ({ work }) => {
  const formattedDate = work.published
    ? new Date(work.published).toLocaleDateString()
    : null

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

  const url = `https://wellcomecollection.org/${
    work.type == 'work' ? 'works' : 'articles'
  }/${work.id}`

  return (
    <>
      <a href={url} className="no-underline">
        <p className="text-xl font-bold">{work.title}</p>
        <div className="text-sm capitalize">
          {formattedDate} - {contributors}
        </div>
        <div className="text-gray-800 text-sm pt-1">{work.standfirst}</div>
      </a>
      <ul className="pt-2 space-x-2">
        {work.concepts.map((concept) => (
          <li key={concept.id} className="inline-block">
            <Link href={`/concepts/${concept.id}`}>
              <a className="no-underline bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700">
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
