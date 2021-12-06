import { ConceptHit, StoryHit } from '../../types/elasticsearch'
import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  parseConcept,
  parseStory,
} from '../../services/elasticsearch'

import blankConceptsQuery from '../../data/queries/concepts.json'
import blankStoriesQuery from '../../data/queries/stories.json'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { query = '', concept, size } = req.query
    const storiesQuery = JSON.parse(
      JSON.stringify(blankStoriesQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      storiesQuery.bool.filter = {
        term: {
          concept_ids: concept,
        },
      }
    }

    const conceptsQuery = JSON.parse(
      JSON.stringify(blankConceptsQuery).replace(/{{query}}/g, query as string)
    )

    try {
      const client = getClient()
      const { body } = await client.msearch({
        body: [
          { index: process.env.ELASTIC_STORIES_INDEX as string },
          { query: storiesQuery, size },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: conceptsQuery, size: 1 },
        ],
      })

      const [storiesResponse, conceptsResponse] = body.responses

      const stories = storiesResponse.hits.hits.map((hit: StoryHit) =>
        parseStory(hit._source)
      )

      const concept = conceptsResponse.hits.hits.map((hit: ConceptHit) =>
        parseConcept(hit._source)
      )

      res.status(200).json({ stories, concept })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}

