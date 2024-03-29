import { FC } from 'react'
import Link from 'next/link'
import { Work } from '../../types/work'

type Props = {
  results: Work[]
}

const WorksResults: FC<Props> = ({ results }) => {
  return (
    <ol className="divide-y">
      {results.map((work) => {
        return (
          <div className="py-4" key={work.id}>
            <Link href={`/works/${work.id}`}>
              <a className="no-underline">
                <div className="pb-1">
                  <span className="bg-paper-2 px-1 py-0.5 text-xs font-semibold capitalize text-black">
                    {work.type ? work.type : 'Work'}
                  </span>
                </div>
                <div className="text-xl font-bold">{work.title}</div>
                <div className="space-x-3 divide-x text-sm">
                  {work.published}
                  {work.contributors && work.published.length > 0 && ' | '}
                  <span className="capitalize">
                    {work.contributors
                      ? work.contributors
                          .map((contributor) => contributor.label)
                          .join(', ')
                      : null}
                  </span>
                </div>
              </a>
            </Link>
          </div>
        )
      })}
    </ol>
  )
}
export default WorksResults
