import { FC } from 'react'
import Link from 'next/link'

export const tabToSlug = {
  Works: 'works',
  Images: 'images',
  Stories: 'stories',
  Subjects: 'subjects',
  People: 'people',
  "What's on": 'whats-on',
}
export const slugToTab = Object.fromEntries(
  Object.entries(tabToSlug).map(([k, v]) => [v, k])
)

export const orderedTabs = Object.keys(tabToSlug) as Array<
  keyof typeof tabToSlug
>
export type Tab = keyof typeof tabToSlug

export function formatNumber(number?: number): string {
  return number ? number.toLocaleString('en-US') : '0'
}

type Props = {
  selectedTab: string
  resultCounts: { [key in Tab]: number }
  queryParams: { [key: string]: string }
}

const Tabs: FC<Props> = ({ queryParams, selectedTab, resultCounts }) => {
  return (
    <ul className="divide-y divide-gray-400 xl:flex xl:divide-y-0 xl:divide-x">
      <Link
        href={{
          pathname: `/search`,
          query: queryParams,
        }}
        key={'overview'}
      >
        <a
          className={`block px-5 py-4 no-underline xl:inline xl:h-full ${
            selectedTab == 'overview' ? 'bg-black text-white' : ''
          }`}
        >
          Overview
        </a>
      </Link>
      {orderedTabs.map((tab) => {
        return (
          <Link
            href={{
              pathname: `/search/${tabToSlug[tab]}`,
              query: queryParams,
            }}
            key={tab}
          >
            <a
              className={`block px-5 py-4 no-underline xl:inline xl:h-full ${
                slugToTab[selectedTab] == tab ? 'bg-black text-white' : ''
              }`}
            >{`${tab} (${formatNumber(resultCounts[tab])})`}</a>
          </Link>
        )
      })}
    </ul>
  )
}

export default Tabs
