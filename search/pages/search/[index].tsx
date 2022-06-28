import { GetServerSideProps, NextPage } from 'next'
import Tabs, { Tab, slugToTab } from '../../components/new/tabs'
import {
  getClient,
  search,
  searchImages,
  searchPeople,
  searchStories,
  searchSubjects,
  searchWhatsOn,
  searchWorks,
} from '../../services/elasticsearch'

import { Concept } from '../../types/concept'
import Head from 'next/head'
import { Image } from '../../types/image'
import ImageResults from '../../components/new/results/images'
import Layout from '../../components/new/layout'
import PeopleResults from '../../components/new/results/people'
import SearchBox from '../../components/new/search-box'
import { Story } from '../../types/story'
import StoryResults from '../../components/new/results/stories'
import SubjectResults from '../../components/new/results/subjects'
import { WhatsOn } from '../../types/whats-on'
import WhatsOnResults from '../../components/new/results/whats-on'
import { Work } from '../../types/work'
import WorkResults from '../../components/new/results/works'

type Props = {
  selectedIndex: string
  searchTerms: string
  resultCounts: { [key in Tab]: number }
  results: Image[] | Work[] | Concept[] | Story[] | Person[] | WhatsOn[]
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const selectedIndex = query.index as string
  const searchTerms = query.query ? query.query.toString() : ''
  const client = getClient()
  const results = await search(selectedIndex, searchTerms, client)

  const resultCounts: { [key in Tab]?: number } = {
    Works: 2065,
    Images: 181,
    Subjects: 0,
    Stories: 5,
    People: 5,
    "What's on": 0,
  }
  return { props: { selectedIndex, searchTerms, resultCounts, results } }
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
          <form>
            <SearchBox searchTerms={searchTerms} />
            <div className="py-6">
              <Tabs
                selectedTab={selectedIndex}
                queryParams={{ query: searchTerms }}
                resultCounts={resultCounts}
              />
            </div>
          </form>
          {selectedIndex === 'works' ? (
            <WorkResults results={results as Work[]} />
          ) : null}
          {selectedIndex === 'people' ? (
            <PeopleResults results={results as Concept[]} />
          ) : null}
          {selectedIndex === 'subjects' ? (
            <SubjectResults results={results as Concept[]} />
          ) : null}
          {selectedIndex === 'stories' ? (
            <StoryResults results={results as Story[]} />
          ) : null}
          {selectedIndex === 'whats-on' ? (
            <WhatsOnResults results={results as WhatsOn[]} />
          ) : null}
        </div>
      </Layout>
      <div className="bg-black">
        <div className="mx-auto px-5 lg:w-3/4">
          {selectedIndex === 'images' ? (
            <ImageResults results={results as Image[]} />
          ) : null}
        </div>
      </div>
    </>
  )
}

export default Search
