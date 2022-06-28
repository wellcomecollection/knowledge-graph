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
      const { query: searchTerms } = req.query
      const client = getClient()
      const resultCounts = await getResultCounts(client, searchTerms as string)

      const results = orderedTabs.reduce(
        (acc, tab) => async () => {
          acc[tab] = search(tab, searchTerms as string, client)
          return acc
        },
        {}
      )
      console.log(results)
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
