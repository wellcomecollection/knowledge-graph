import { FC } from 'react'
import Link from 'next/link'

export const tabToSlug = {
  Works: 'works',
  Images: 'images',
  Stories: 'stories',
  "What's on": 'whats-on',
}
export const slugToTab = Object.fromEntries(
  Object.entries(tabToSlug).map(([k, v]) => [v, k])
)

export const orderedTabs = Object.keys(tabToSlug) as Array<
  keyof typeof tabToSlug
>
export type Tab = keyof typeof tabToSlug
export type Slug = keyof typeof slugToTab

export function formatNumber(number?: number): string {
  return number ? number.toLocaleString('en-US') : '0'
}

type Props = {
  selectedTab: string
  resultCounts: { [key in Tab]: number }
  queryParams: { [key: string]: string }
}

const Tabs: FC<Props> = ({ queryParams, selectedTab, resultCounts }) => {
  let paramsToPass = {}
  if (queryParams.searchTerms) {
    paramsToPass = { ...paramsToPass, query: queryParams.searchTerms }
  }
  if (queryParams.subject) {
    paramsToPass = { ...paramsToPass, subject: queryParams.subject }
  }
  if (queryParams.person) {
    paramsToPass = { ...paramsToPass, person: queryParams.person }
  }
  return (
    <ul className="flex divide-gray-400 border-b">
      <Link
        href={{
          pathname: `/search`,
          query: paramsToPass,
        }}
        key={'overview'}
      >
        <a
          className={`inline h-full border-yellow px-5 py-3 no-underline ${
            selectedTab == 'overview' ? 'border-b-4' : ''
          }`}
        >
          <span className="font-bold">Overview</span>
        </a>
      </Link>
      {orderedTabs.map((tab) => {
        return (
          <Link
            href={{
              pathname: `/search/${tabToSlug[tab]}`,
              query: paramsToPass,
            }}
            key={tab}
          >
            <a
              className={`inline h-full border-yellow px-5 py-3 no-underline  ${
                slugToTab[selectedTab] == tab ? 'border-b-4 ' : ''
              }`}
            >
              <div>
                <span className="font-bold">{tab}</span>
                <span className="text-sm text-gray-700">{` (${formatNumber(
                  resultCounts[tab]
                )})`}</span>
              </div>
            </a>
          </Link>
        )
      })}
    </ul>
  )
}

export default Tabs
