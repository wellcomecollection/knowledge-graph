import { FC } from 'react'
import { Image } from '../../types/image'

type Props = {
  results: Image[]
}

const ImageResults: FC<Props> = ({ results }) => {
  return (
    <ol className=" columns-3 lg:columns-4 xl:columns-5 space-y-2 p-5">
      {results.map((image) => {
        return (
          <li key={image.id}>
            <img src={image.url} alt={image.title} />
          </li>
        )
      })}
    </ol>
  )
}
export default ImageResults
