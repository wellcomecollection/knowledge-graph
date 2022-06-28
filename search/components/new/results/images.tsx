import { FC } from 'react'
import { Image } from '../../../types/image'

type Props = {
  results: Image[]
}

const ImageResults: FC<Props> = ({ results }) => {
  return (
    <ol className="grid grid-cols-2 gap-x-3 gap-y-5 py-8 lg:grid-cols-3 lg:gap-y-3 xl:grid-cols-4">
      {results.map((image) => {
        return (
          <li key={image.id} className="relative pb-3/4">
            <img
              src={image.url}
              alt={image.title}
              className="absolute h-full w-full object-cover"
            />
          </li>
        )
      })}
    </ol>
  )
}
export default ImageResults
