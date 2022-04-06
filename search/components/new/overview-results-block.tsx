import { ArrowRight } from 'react-feather'
import { FC } from 'react'
import { formatNumber } from './tabs'

type Props = {
  name: string
  totalResults: number
}

const OverviewResultsBlock: FC<Props> = ({ name, totalResults, children }) => {
  return (
    <>
      <h2>{name}</h2>
      <div className="py-4">{children}</div>
      <a href="" className="bg-gray-200 py-2 px-3 no-underline">
        All {name.toLowerCase()} ({formatNumber(totalResults)}){' '}
        <ArrowRight className="inline-block w-4" />
      </a>
    </>
  )
}
export default OverviewResultsBlock
