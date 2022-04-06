import Layout from '../../components/new/layout'
import { NextPage } from 'next'
import OverviewResultsBlock from '../../components/new/overview-results-block'
import SearchBox from '../../components/new/search-box'
import Tabs from '../../components/new/tabs'

export const getServerSideProps: GetServerSideProps<Props> = async ({
  query: qs,
  req,
}) => {
  // parse the query string
  const tab = qs.tab ? qs.tab.toString() : 'Overview'
  const query = qs.query ? qs.query.toString() : ''
  return { props: { tab, query } }
}
const Collections: NextPage = ({ tab, query }) => {
  const nResults = {
    Collections: 31965,
    Images: 12,
    Stories: 0,
    'Exhibitions & Events': 0,
  }
  const orderedSections = [
    'Exhibitions & Events',
    'Stories',
    'Collections',
    'Images',
  ]
  return (
    <Layout isHomePage>
      <div className="mx-auto px-5 md:w-4/5 md:px-12 xl:w-3/4">
        <form>
          <SearchBox query={query} />
          <div className="py-6">
            <Tabs selected={tab} nResults={nResults} />
          </div>
        </form>
        <ul className="space-y-8 divide-y">
          {orderedSections.map((section) => (
            <li key={section} className="py-4">
              <OverviewResultsBlock
                name={section}
                totalResults={nResults[section]}
              />
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  )
}

export default Collections
