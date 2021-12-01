import { FC } from 'react'
import { Hit as HitType } from '../../types/elasticsearch'

type Props = { hit: HitType }
const Hit: FC<Props> = ({ hit }) => {
  const formattedDate = new Date(hit._source.published).toLocaleDateString()
  const url = `https://wellcomecollection.org/articles/${hit._source.wellcome_id}`
  const concepts = hit._source.concepts.split(',')
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
        <div className=" text-sm pt-2">{concepts.join(', ')}</div>
      </a>
    </>
  )
}

export default Hit
