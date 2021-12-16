import { FC } from 'react'
import Link from 'next/link'
import { Story } from '../types/elasticsearch'

type Props = { story: Story }
const SearchResult: FC<Props> = ({ story }) => {
  const formattedDate = new Date(story.published).toLocaleDateString()
  const url = `https://wellcomecollection.org/articles/${story.id}`

  return (
    <>
      <a href={url} className="no-underline">
        <p className="text-xl font-bold">{story.title}</p>
        <div className="text-sm capitalize">
          {formattedDate} -{' '}
          {story.contributors
            .map<React.ReactNode>((contributor) => {
              return (
                <span key={contributor.id}>
                  <a
                    className="no-underline"
                    href={`/people/${contributor.id}`}
                  >
                    {contributor.name}
                  </a>
                </span>
              )
            })
            .reduce((acc, curr) => [acc, ', ', curr])}
        </div>
        <div className="text-gray-800 text-sm pt-1">{story.standfirst}</div>
      </a>
      <ul className="pt-2 space-x-2">
        {story.concepts.map((concept) => (
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
