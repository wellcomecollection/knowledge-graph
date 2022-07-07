import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Tab, orderedTabs } from '../../components/tabs'

import Head from 'next/head'
import { Image } from '../../types/image'
import ImageResultsOverview from '../../components/results/overview/images'
import Layout from '../../components/layout'
import OverviewResultsBlock from '../../components/results/overview'
import SearchBox from '../../components/search-box'
import { Story } from '../../types/story'
import StoryResultsOverview from '../../components/results/overview/stories'
import { WhatsOn } from '../../types/whats-on'
import WhatsOnResultsOverview from '../../components/results/overview/whats-on'
import { Work } from '../../types/work'
import WorkResultsOverview from '../../components/results/overview/works'

type Props = {
  searchTerms: string
  resultCounts: { [key in Tab]: number }
  results: { [key in Tab]: Image[] | Work[] | Story[] | WhatsOn[] }
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const searchTerms = query.query ? query.query.toString() : ''
  const url = `${process.env.VERCEL_URL}/api/search?query=${searchTerms}`
  const { results, resultCounts } = await fetch(url).then((res) => res.json())
  return { props: { searchTerms, results, resultCounts } }
}

const Search: NextPage<Props> = ({ searchTerms, resultCounts, results }) => {
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
          <ol className="divide-y">
            {resultCounts["What's on"] > 0 ? (
              <li className="pb-8 pt-2">
                <WhatsOnResultsOverview
                  results={results["What's on"] as WhatsOn[]}
                  queryParams={{ query: searchTerms }}
                  totalResults={resultCounts["What's on"]}
                />
              </li>
            ) : null}
            {resultCounts.Stories > 0 ? (
              <li className="pb-8 pt-2">
                <StoryResultsOverview
                  results={results.Stories as Story[]}
                  queryParams={{ query: searchTerms }}
                  totalResults={resultCounts.Stories}
                />
              </li>
            ) : null}
            {resultCounts.Works > 0 ? (
              <li className="pb-8 pt-2">
                <WorkResultsOverview
                  results={results.Works as Work[]}
                  queryParams={{ query: searchTerms }}
                  totalResults={resultCounts.Works}
                />
              </li>
            ) : null}
            {resultCounts.Images > 0 ? (
              <li className="pb-8 pt-2">
                <ImageResultsOverview
                  results={results.Images as Image[]}
                  queryParams={{ query: searchTerms }}
                  totalResults={resultCounts.Images}
                />
              </li>
            ) : null}
          </ol>
        </div>
      </Layout>
    </>
  )
}

export default Search
