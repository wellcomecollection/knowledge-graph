import { NextApiRequest, NextApiResponse } from 'next'
import { Tab, orderedTabs, tabToSlug } from '../../../components/tabs'
import { getClient, getResultCounts, search } from '../../../services'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const { query: searchTerms } = req.query
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
