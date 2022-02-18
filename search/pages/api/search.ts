import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  parseConcept,
  parseStory,
  parseWork,
} from '../../services/elasticsearch'

import { ConceptHit } from '../../types/concept'
import { StoryHit } from '../../types/story'
import { WorkHit } from '../../types/work'
import blankConceptsQuery from '../../data/queries/concepts.json'
import blankPeopleQuery from '../../data/queries/people.json'
import blankStoriesQuery from '../../data/queries/stories.json'
import blankWorksQuery from '../../data/queries/works.json'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { query = '', concept, person, size = '10', page = '1' } = req.query
    const from = (parseInt(page as string) - 1) * parseInt(size as string)

    const worksQuery = JSON.parse(
      JSON.stringify(blankWorksQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      worksQuery.bool.filter.push({
        term: {
          concept_ids: concept,
        },
      })
    }
    if (person) {
      worksQuery.bool.filter.push({
        term: {
          contributor_ids: person,
        },
      })
    }

    const storiesQuery = JSON.parse(
      JSON.stringify(blankStoriesQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      worksQuery.bool.filter.push({
        term: {
          concept_ids: concept,
        },
      })
    }
    if (person) {
      worksQuery.bool.filter.push({
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
          { index: process.env.ELASTIC_WORKS_INDEX as string },
          { query: worksQuery, size, from },
          { index: process.env.ELASTIC_STORIES_INDEX as string },
          { query: storiesQuery, size, from },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: conceptsQuery, size: 1 },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: peopleQuery, size: 1 },
        ],
      })
      const [worksResponse, storiesResponse, conceptsResponse, peopleResponse] =
        body.responses

      res.status(200).json({
        works: {
          results: worksResponse.hits.hits.map((hit: WorkHit) =>
            parseWork(hit)
          ),
          total: worksResponse.hits.total.value,
        },
        stories: {
          results: storiesResponse.hits.hits.map((hit: StoryHit) =>
            parseStory(hit)
          ),
          total: storiesResponse.hits.total.value,
        },
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
