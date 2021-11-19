import { FC } from 'react'
import { Hit as HitType } from '../types/elasticsearch'

type Props = { hit: HitType }
const Hit: FC<Props> = ({ hit }) => {
  return (
    <div>
      <a href={hit._source.URL}>
        <h2>{hit._source.Title}</h2>
      </a>
      <div>{hit._source.Author}</div>
    </div>
  )
}

export default Hit
