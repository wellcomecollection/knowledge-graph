import { NextApiRequest, NextApiResponse } from 'next'
import {
  Tab,
  orderedTabs,
  slugToTab,
  tabToSlug,
} from '../../../components/tabs'
import {
  getClient,
  getResultCounts,
  search,
  searchImages,
  searchStories,
  searchWhatsOn,
  searchWorks,
} from '../../../services/elasticsearch'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const { query: searchTerms, index: selectedIndex } = req.query
      const client = getClient()
      const resultCounts = await getResultCounts(client, searchTerms as string)

      const results = {} as { [key in Tab]: any[] }
      results[slugToTab[selectedIndex as string] as Tab] = await search(
        selectedIndex as string,
        searchTerms as string,
        client,
        10
      )
      res.status(200).json({
        results,
        resultCounts,
      })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
