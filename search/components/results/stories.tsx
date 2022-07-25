import { FC } from 'react'
import Link from 'next/link'
import { Story } from '../../types/story'
import { formatDate } from '.'

type Props = {
  results: Story[]
}

const StoryResults: FC<Props> = ({ results }) => {
  return (
    <ol className="divide-y">
      {results.map((story) => {
        return (
          <div key={story.id} className="py-4">
            <Link href={`https://wellcomecollection.org/articles/${story.id}`}>
              <a className="no-underline">
                <div className="pb-1">
                  <span className="bg-paper-3 px-1 py-0.5 text-xs font-semibold capitalize text-black">
                    {story.type ? story.type : 'Story'}
                  </span>
                </div>
                <div className="text-xl font-bold">
                  {story.title}
                </div>
                <p className="py-1 capitalize text-gray-700">
                  {story.published ? formatDate(story.published) : null}
                  {story.contributors &&
                    formatDate(story.published).length > 0 &&
                    ' | '}
                  {story.contributors
                    ? story.contributors
                        .map((contributor) => contributor.label)
                        .join(', ')
                    : null}
                </p>
                <p>{story.standfirst}</p>
              </a>
            </Link>
          </div>
        )
      })}
    </ol>
  )
}

export default StoryResults
