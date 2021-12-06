import { NextApiRequest, NextApiResponse } from 'next'

import { ApiResponse } from '@elastic/elasticsearch'
import conceptsFilter from '../../data/queries/conceptsFilter.json'
import { getClient } from '../../services/elasticsearch'
import storiesQuery from '../../data/queries/stories.json'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { query = '', concept, size } = req.query
    const queryBody = JSON.parse(
      JSON.stringify(storiesQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      queryBody.bool.filter.push(
        JSON.parse(
          JSON.stringify(conceptsFilter).replace(
            /{{query}}/g,
            concept as string
          )
        )
      )
    }

    await getClient()
      .search({
        index: process.env.ELASTIC_STORIES_INDEX as string,
        body: { query: queryBody, size },
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
