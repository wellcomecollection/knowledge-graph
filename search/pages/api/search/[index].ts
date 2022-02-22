import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  parseConcept,
  parseStory,
  parseWork,
} from '../../../services/elasticsearch'

import { ConceptHit } from '../../../types/concept'
import { StoryHit } from '../../../types/story'
import { WorkHit } from '../../../types/work'
import blankConceptsQuery from '../../../data/queries/concepts.json'
import blankPeopleQuery from '../../../data/queries/people.json'
import blankStoriesQuery from '../../../data/queries/stories.json'
import blankWorksQuery from '../../../data/queries/works.json'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { index, query = '', concept, person, page = '1' } = req.query
    const blankQuery = { works: blankWorksQuery, stories: blankStoriesQuery }[
      index as string
    ]
    const chosenIndex = {
      works: process.env.ELASTIC_WORKS_INDEX,
      stories: process.env.ELASTIC_STORIES_INDEX,
    }[index as string]

    const structuredQuery = JSON.parse(
      JSON.stringify(blankQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      structuredQuery.bool.filter.push({
        term: {
          concept_ids: concept,
        },
      })
    }
    if (person) {
      structuredQuery.bool.filter.push({
        term: {
          contributor_ids: person,
        },
      })
    }

    const conceptsQuery = JSON.parse(
      JSON.stringify(blankConceptsQuery).replace(/{{query}}/g, query as string)
    )
    const peopleQuery = JSON.parse(
      JSON.stringify(blankPeopleQuery).replace(/{{query}}/g, query as string)
    )

    try {
      const { body } = await getClient().msearch({
        body: [
          { index: chosenIndex },
          {
            query: structuredQuery,
            size:10,
            from: (parseInt(page as string) - 1) * 10,
          },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: conceptsQuery, size: 1 },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: peopleQuery, size: 1 },
        ],
      })
      const [response, conceptsResponse, peopleResponse] = body.responses

      const results = response.hits.hits.map((hit: WorkHit | StoryHit) => {
        if (index === 'works') {
          return parseWork(hit as WorkHit)
        } else if (index === 'stories') {
          return parseStory(hit as StoryHit)
        }
      })

      res.status(200).json({
        results: results,
        total: response.hits.total.value,
        concept: conceptsResponse.hits.hits.map((hit: ConceptHit) =>
          parseConcept(hit)
        ),
        person: peopleResponse.hits.hits.map((hit: ConceptHit) =>
          parseConcept(hit)
        ),
      })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
