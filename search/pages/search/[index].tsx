import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Tab, slugToTab } from '../../components/tabs'
import {
  getClient,
  getResultCounts,
  search,
} from '../../services/elasticsearch'

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
  searchTerms: string
  resultCounts: any
  results: Image[] | Work[] | Story[] | WhatsOn[]
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const selectedIndex = query.index as string

  // if the user hasn't provided a search term, return an empty set of results
  if (!query.query) {
    return {
      props: {
        selectedIndex,
        searchTerms: '',
        resultCounts: {
          images: 0,
          works: 0,
          stories: 0,
          whatsOn: 0,
        },
        results: [],
      },
    }
  } else {
    const searchTerms = query.query.toString()
    const client = getClient()
    const resultCounts = await getResultCounts(client, searchTerms as string)
    const results = await search(
      selectedIndex as string,
      searchTerms as string,
      client,
      10
    )
    return { props: { selectedIndex, searchTerms, resultCounts, results } }
  }
}

const Search: NextPage<Props> = ({
  selectedIndex,
  searchTerms,
  resultCounts,
  results,
}) => {
  return (
    <>
      <Head>
        <title>{`${slugToTab[selectedIndex]} | ${searchTerms}`}</title>
      </Head>
      <Layout isHomePage>
        <div className="mx-auto px-5 lg:w-3/4">
          <SearchBox searchTerms={searchTerms} index={selectedIndex} />
          <div className="py-6">
            <Tabs
              selectedTab={selectedIndex}
              queryParams={{ query: searchTerms }}
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
            <ImageResults results={results as Image[]} />
          ) : null}
        </div>
      </div>
    </>
  )
}

export default Search
