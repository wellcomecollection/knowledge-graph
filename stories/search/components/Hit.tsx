import { FC } from 'react'
import { Hit as HitType } from '../types/elasticsearch'

type Props = { hit: HitType }
const Hit: FC<Props> = ({ hit }) => {
  const formattedDate = new Date(
    hit._source['Date published']
  ).toLocaleDateString()
  return (
    <>
      <a href={hit._source.URL} className="no-underline">
        <p className="text-xl font-bold">{hit._source.Title}</p>
        <div className="text-sm">
          {hit._source.Author},{' '}
          {hit._source['Images by'] ? hit._source['Images by'] + ',' : ''}{' '}
          {formattedDate}
        </div>
        <div className="text-gray-800 text-sm pt-2">
          {hit._source.standfirst}
        </div>
      </a>
    </>
  )
}

export default Hit
