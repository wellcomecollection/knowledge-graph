import { formatNumber, tabToSlug } from '../../tabs'

import { ArrowRight } from 'react-feather'
import { FC } from 'react'
import Link from 'next/link'

type Props = {
  name: string
  totalResults: number
  queryParams: { [key: string]: string }
}

const OverviewResultsBlock: FC<Props> = ({
  name,
  totalResults,
  queryParams,
  children,
}) => {
  return (
    <>
      <h2>{name}</h2>
      <div className="py-4">{children}</div>
      <Link
        href={{
          pathname: `/search/${tabToSlug[name]}`,
          query: queryParams,
        }}
      >
        <a className="bg-gray-200 py-2 px-3 no-underline">
          All {name.toLowerCase()} ({formatNumber(totalResults)}){' '}
          <ArrowRight className="inline-block w-4" />
        </a>
      </Link>
    </>
  )
}
export default OverviewResultsBlock
