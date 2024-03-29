import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Slug, Tab, slugToTab } from '../../components/tabs'
import { filter, getClient, getResultCounts, search } from '../../services'

import Head from 'next/head'
import { Image } from '../../types/image'
import ImageResults from '../../components/results/images'
import Layout from '../../components/layout'
import SearchBox from '../../components/search-box'
import { Story } from '../../types/story'
import StoryResults from '../../components/results/stories'
import { WhatsOn } from '../../types/whats-on'
import WhatsOnResults from '../../components/results/whats-on'
import { Work } from '../../types/work'
import WorksResults from '../../components/results/works'

type Props = {
  selectedIndex: string
  queryParams?: {
    searchTerms?: string
    subject?: string
    person?: string
  }
  resultCounts: { [key in Tab]: number }
  results: Image[] | Work[] | Story[] | WhatsOn[]
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const selectedIndex = query.index as string

  // if the user hasn't provided a search term, return an empty set of results
  if (query.query) {
    const searchTerms = query.query.toString()
    const client = getClient()
    const resultCounts = await getResultCounts(client, searchTerms as string)
    const results = await search(
      selectedIndex as string,
      searchTerms as string,
      client,
      10
    )
    return {
      props: {
        selectedIndex,
        queryParams: { searchTerms },
        resultCounts,
        results,
      },
    }
  } // if they're filtering by a subject or person, use filter() instead
  else if (query.subject) {
    const client = getClient()
    const { results, resultCount } = await filter(
      client,
      selectedIndex as string,
      query.subject as string
    )
    let resultCounts = {
      Images: 0,
      Works: 0,
      Stories: 0,
      "What's on": 0,
    }
    resultCounts[slugToTab[selectedIndex] as Tab] = resultCount
    return {
      props: {
        selectedIndex,
        queryParams: { subject: query.subject },
        resultCounts,
        results,
      },
    }
  } else if (query.person) {
    const client = getClient()
    const { results, resultCount } = await filter(
      client,
      selectedIndex as string,
      query.person as string
    )
    let resultCounts = {
      Images: 0,
      Works: 0,
      Stories: 0,
      "What's on": 0,
    }
    resultCounts[slugToTab[selectedIndex] as Tab] = resultCount
    return {
      props: {
        selectedIndex,
        queryParams: { person: query.person },
        resultCounts,
        results,
      },
    }
  } // if they're not searching, return an empty set of results
  else {
    return {
      props: {
        selectedIndex,
        queryParams: {},
        resultCounts: {
          Images: 0,
          Works: 0,
          Stories: 0,
          "What's on": 0,
        },
        results: [],
      },
    }
  }
}

const Search: NextPage<Props> = ({
  selectedIndex,
  queryParams,
  resultCounts,
  results,
}) => {
  return (
    <>
      <Head>
        <title>{`${slugToTab[selectedIndex]}${
          queryParams
            ? queryParams.searchTerms
              ? ` | ${queryParams.searchTerms}`
              : ''
            : ''
        }`}</title>
      </Head>
      <Layout isHomePage>
        <div className="mx-auto px-5 lg:w-3/4">
          <SearchBox
            queryParams={{
              ...queryParams,
            }}
            index={selectedIndex}
          />
          <div className="py-6">
            <Tabs
              selectedTab={selectedIndex}
              queryParams={{ ...queryParams }}
              resultCounts={resultCounts}
            />
          </div>
          {selectedIndex === 'works' ? (
            <WorksResults results={results as Work[]} />
          ) : null}
          {selectedIndex === 'stories' ? (
            <StoryResults results={results as Story[]} />
          ) : null}
          {selectedIndex === 'whats-on' ? (
            <WhatsOnResults results={results as WhatsOn[]} />
          ) : null}
        </div>
      </Layout>
      <div className="bg-gray-900">
        <div className="mx-auto lg:w-3/4">
          {selectedIndex === 'images' ? (
            <div className="p-5">
              <ImageResults results={results as Image[]} />
            </div>
          ) : null}
        </div>
      </div>
    </>
  )
}

export default Search
