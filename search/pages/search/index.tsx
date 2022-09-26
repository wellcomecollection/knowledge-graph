import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Tab, orderedTabs, tabToSlug } from '../../components/tabs'
import { getClient, getResultCounts, search } from '../../services'

import Head from 'next/head'
import { Image } from '../../types/image'
import ImageResultsOverview from '../../components/results/overview/images'
import Layout from '../../components/layout'
import SearchBox from '../../components/search-box'
import { Story } from '../../types/story'
import StoryResultsOverview from '../../components/results/overview/stories'
import { WhatsOn } from '../../types/whats-on'
import WhatsOnResultsOverview from '../../components/results/overview/whats-on'
import { Work } from '../../types/work'
import WorkResultsOverview from '../../components/results/overview/works'

type Props = {
  queryParams: { searchTerms: string }
  resultCounts: { [key in Tab]: number }
  results: { [key in Tab]: Image[] | Work[] | Story[] | WhatsOn[] }
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  if (!query.query) {
    return {
      props: {
        queryParams: { searchTerms: '' },
        resultCounts: {
          images: 0,
          works: 0,
          stories: 0,
          whatsOn: 0,
        },
        results: {
          images: [],
          works: [],
          stories: [],
          whatsOn: [],
        },
      },
    }
  } else {
    const searchTerms = query.query.toString()
    const client = getClient()
    const resultCounts = await getResultCounts(client, searchTerms as string)
    const results = {} as { [key in Tab]: any[] }
    for (const tab of orderedTabs) {
      results[tab] = await search(
        tabToSlug[tab],
        searchTerms as string,
        client,
        3
      )
    }
    return { props: { queryParams: { searchTerms }, results, resultCounts } }
  }
}

const Search: NextPage<Props> = ({ queryParams, resultCounts, results }) => {
  return (
    <>
      <Head>
        <title>{`Search  ${
          queryParams.searchTerms ? `| ${queryParams.searchTerms}` : ''
        }`}</title>
      </Head>
      <Layout isHomePage>
        <div className="mx-auto px-5 lg:w-3/4">
          <SearchBox queryParams={queryParams} />
          <div className="pt-6">
            <Tabs
              selectedTab={'overview'}
              queryParams={{ ...queryParams }}
              resultCounts={resultCounts}
            />
          </div>
          <ol>
            {resultCounts["What's on"] > 0 ? (
              <li className="py-8">
                <WhatsOnResultsOverview
                  results={results["What's on"] as WhatsOn[]}
                  queryParams={queryParams}
                  totalResults={resultCounts["What's on"]}
                />
              </li>
            ) : null}
            {resultCounts.Stories > 0 ? (
              <li className="pt-8 pb-4">
                <StoryResultsOverview
                  results={results.Stories as Story[]}
                  queryParams={queryParams}
                  totalResults={resultCounts.Stories}
                />
              </li>
            ) : null}
            {resultCounts.Works > 0 ? (
              <li className="pt-8 pb-4">
                <WorkResultsOverview
                  results={results.Works as Work[]}
                  queryParams={queryParams}
                  totalResults={resultCounts.Works}
                />
              </li>
            ) : null}
            {resultCounts.Images > 0 ? (
              <li className="pt-8 pb-4">
                <ImageResultsOverview
                  results={results.Images as Image[]}
                  queryParams={queryParams}
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
