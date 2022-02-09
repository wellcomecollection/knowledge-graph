import { ConceptHit, WorkHit } from '../../types/elasticsearch'
import { NextApiRequest, NextApiResponse } from 'next'
import {
  getClient,
  parseConcept,
  parseWork,
} from '../../services/elasticsearch'

import blankConceptsQuery from '../../data/queries/concepts.json'
import blankPeopleQuery from '../../data/queries/people.json'
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
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: conceptsQuery, size: 1 },
          { index: process.env.ELASTIC_CONCEPTS_INDEX as string },
          { query: peopleQuery, size: 1 },
        ],
      })
      const [worksResponse, conceptsResponse, peopleResponse] = body.responses
      const total = worksResponse.hits.total.value
      const worksResults = worksResponse.hits.hits.map((hit: WorkHit) =>
        parseWork(hit)
      )
      const concept = conceptsResponse.hits.hits.map((hit: ConceptHit) =>
        parseConcept(hit)
      )
      const person = peopleResponse.hits.hits.map((hit: ConceptHit) =>
        parseConcept(hit)
      )
      res
        .status(200)
        .json({ works: { results: worksResults, total }, concept, person })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
