import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Tab, orderedTabs, slugToTab } from '../../components/new/tabs'

import Head from 'next/head'
import Layout from '../../components/new/layout'
import OverviewResultsBlock from '../../components/new/results/overview'
import SearchBox from '../../components/new/search-box'

type Props = {
  searchTerms: string
  resultCounts: { [key in Tab]: number }
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const searchTerms = query.query ? query.query.toString() : ''
  const resultCounts: { [key in Tab]?: number } = {
    Works: 2065,
    Images: 181,
    Subjects: 0,
    Stories: 5,
    People: 5,
    "What's on": 0,
  }
  return { props: { searchTerms, resultCounts } }
}

const Search: NextPage<Props> = ({ searchTerms, resultCounts }) => {
  return (
    <>
      <Head>
        <title>{`Search  ${searchTerms ? `| ${searchTerms}` : ''}`}</title>
      </Head>
      <Layout isHomePage>
        <div className="mx-auto px-5 lg:w-3/4">
          <form>
            <SearchBox searchTerms={searchTerms} />
            <div className="py-6">
              <Tabs
                selectedTab={'overview'}
                queryParams={{ query: searchTerms }}
                resultCounts={resultCounts}
              />
            </div>
          </form>
          <ul className="space-y-8 divide-y">
            {orderedTabs.map((tab) =>
              resultCounts[tab] ? (
                <li key={tab} className="py-4">
                  <OverviewResultsBlock
                    name={tab}
                    totalResults={resultCounts[tab]}
                  />
                </li>
              ) : null
            )}
          </ul>
        </div>
      </Layout>
    </>
  )
}

export default Search
