import { Tab, formatNumber, tabToSlug, Slug } from '../../tabs'

import { ArrowRight } from 'react-feather'
import { FC } from 'react'
import Link from 'next/link'

type Props = {
  index: string
  heading: string
  totalResults: number
  queryParams?: { [key: string]: string }
}

const OverviewResultsBlock: FC<Props> = ({
  index,
  heading,
  totalResults,
  queryParams,
  children,
}) => {
  return (
    <>
      <h2 className="font-sans font-light">{heading}</h2>
      <div>{children}</div>
      <div className="pt-4">
        <Link
          href={{
            pathname: `/search/${index as Slug}`,
            query: queryParams,
          }}
        >
          <a className="bg-gray-200 py-2 px-3 no-underline">
            All {index.toLowerCase()} ({formatNumber(totalResults)}){' '}
            <ArrowRight className="inline-block w-4" />
          </a>
        </Link>
      </div>
    </>
  )
}
export default OverviewResultsBlock
