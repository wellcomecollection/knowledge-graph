import { Concept } from '../../../types/concept'
import { FC } from 'react'

type Props = {
  results: Concept[]
}

const SubjectResults: FC<Props> = ({ results }) => {
  return (
    <ol>
      {results.map((concept) => {
        return (
          <div key={concept.id}>
            <h2>{concept.preferred_name}</h2>
          </div>
        )
      })}
    </ol>
  )
}
export default SubjectResults
