import { FC } from 'react'
import { Hit as HitType } from '../types/elasticsearch'
import Link from 'next/link'

type Props = { hit: HitType }
const Hit: FC<Props> = ({ hit }) => {
  const formattedDate = new Date(hit._source.published).toLocaleDateString()
  const url = `https://wellcomecollection.org/articles/${hit._source.wellcome_id}`
  const concepts = hit._source.concepts.split(',')
  const concept_ids = hit._source.concept_ids.split(',')
  const contributors = hit._source.contributors.split(',')
  return (
    <>
      <a href={url} className="no-underline">
        <p className="text-xl font-bold">{hit._source.title}</p>
        <div className="text-sm">
          {formattedDate} - {contributors.join(', ')}
        </div>
        <div className="text-gray-800 text-sm pt-2">
          {hit._source.standfirst}
        </div>
      </a>
      <ul className="pt-2 space-x-2">
        {concepts.map((concept, index) => (
          <li key={concept} className="inline-block">
            <Link href={`/concepts/${concept_ids[index]}`}>
              <a className="no-underline bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700">
                {concept}
              </a>
            </Link>
          </li>
        ))}
      </ul>
    </>
  )
}

export default Hit
