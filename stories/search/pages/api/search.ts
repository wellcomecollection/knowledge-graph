import { ConceptHit, PersonHit, StoryHit } from '../../types/elasticsearch'
import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  parseConcept,
  parsePerson,
  parseStory,
} from '../../services/elasticsearch'

import blankConceptsQuery from '../../data/queries/concepts.json'
import blankPeopleQuery from '../../data/queries/people.json'
import blankStoriesQuery from '../../data/queries/stories.json'

export default async function search(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { query = '', concept, person, size = '10', page = '1' } = req.query
    const from = (parseInt(page as string) - 1) * parseInt(size as string)

    const storiesQuery = JSON.parse(
      JSON.stringify(blankStoriesQuery).replace(/{{query}}/g, query as string)
    )
    if (concept) {
      storiesQuery.bool.filter.push({
        term: {
          concept_ids: concept,
        },
      })
    }
    if (person) {
      storiesQuery.bool.filter.push({
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
          { index: process.env.ELASTIC_STORIES_INDEX as string },
          { query: storiesQuery, size, from },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: conceptsQuery, size: 1 },
          { index: process.env.ELASTIC_PEOPLE_INDEX as string },
          { query: peopleQuery, size: 1 },
        ],
      })
      const [storiesResponse, conceptsResponse, peopleResponse] = body.responses
      const total = storiesResponse.hits.total.value
      const storiesResults = storiesResponse.hits.hits.map((hit: StoryHit) =>
        parseStory(hit)
      )
      const concept = conceptsResponse.hits.hits.map((hit: ConceptHit) =>
        parseConcept(hit)
      )
      const person = peopleResponse.hits.hits.map((hit: PersonHit) =>
        parsePerson(hit)
      )
      res
        .status(200)
        .json({ stories: { results: storiesResults, total }, concept, person })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
