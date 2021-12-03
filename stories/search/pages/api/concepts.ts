import { NextApiRequest, NextApiResponse } from 'next'

import { ApiResponse } from '@elastic/elasticsearch'
import conceptsQuery from '../../data/queries/concepts.json'
import { getClient } from '../../services/elasticsearch'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { q, size } = req.query
    if (!q) {
      res.status(500).json({ error: 'Missing query parameter q' })
      return
    }

    const query = JSON.parse(
      JSON.stringify(conceptsQuery).replace(/{{query}}/g, q as string)
    )
    await getClient()
      .search({
        index: process.env.ELASTIC_CONCEPTS_INDEX as string,
        body: { query, size },
      })
      .then((result: ApiResponse) => {
        res.status(200).json(result.body.hits)
      })
      .catch(() => {
        res.status(500).json({ error: 'Unable to query' })
      })
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
