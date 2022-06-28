import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  getResultCounts,
  search,
  searchImages,
  searchPeople,
  searchStories,
  searchSubjects,
  searchWhatsOn,
  searchWorks,
} from '../../../services/elasticsearch'
import { orderedTabs, slugToTab, tabToSlug } from '../../../components/new/tabs'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const { query: searchTerms, index: selectedIndex } = req.query
      const client = getClient()
      const resultCounts = await getResultCounts(client, searchTerms as string)


      const results = orderedTabs.reduce((acc, tab) => {
        acc[tab] = []
        return acc
      }, {})

      const tab = slugToTab[selectedIndex as string]
      console.log(tab)
      results[tab] = await search(
        selectedIndex as string,
        searchTerms as string,
        client,
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
