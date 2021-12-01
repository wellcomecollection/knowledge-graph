import { FC } from 'react'
import { Hit as HitType } from '../types/elasticsearch'

type Props = { hit: HitType }
const Hit: FC<Props> = ({ hit }) => {
  const formattedDate = new Date(hit._source.published).toLocaleDateString()
  const url = `https://wellcomecollection.org/articles/${hit._source.wellcome_id}`
  return (
    <>
      <a href={url} className="no-underline">
        <p className="text-xl font-bold">{hit._source.title}</p>
        <div className="text-sm">
          <p>{hit._source.contributors}</p>
          <p>{formattedDate}</p>
        </div>
        <div className="text-gray-800 text-sm pt-2">
          {hit._source.standfirst}
        </div>
      </a>
    </>
  )
}

export default Hit
