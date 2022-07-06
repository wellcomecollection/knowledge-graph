import { FC } from 'react'
import { Image } from '../../../types/image'
import OverviewResultsBlock from '.'

type Props = {
  totalResults: number
  queryParams: any
  results: Image[]
}
const ImageResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
}) => {
  return (
    <OverviewResultsBlock
      name="Images"
      totalResults={totalResults}
      queryParams={queryParams}
    >
      <ul className="grid grid-cols-2 gap-2 md:grid-cols-3 xl:grid-cols-5">
        {results.map((image) => (
          <li key={image.id} className="relative pb-3/4">
            <img
              src={image.url}
              alt={image.title}
              className="absolute h-full w-full object-cover"
            />
          </li>
        ))}
      </ul>
    </OverviewResultsBlock>
  )
}

export default ImageResultsOverview
