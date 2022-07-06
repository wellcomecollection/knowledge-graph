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
                    {work.type}
                  </span>
                </div>
                <div className="text-xl font-bold">{work.title}</div>
                <p className="capitalize">
                  {work.contributors
                    .map((contributor) => contributor.name)
                    .join(', ')}
                </p>
              </a>
            </Link>
          </div>
        )
      })}
    </ol>
  )
}
export default WorksResults
