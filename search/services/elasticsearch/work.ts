import { Work, WorkHit } from '../../types/work'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/works.json'
import { formatQuery } from '.'

export function parseWork(workHit: WorkHit): Work {
  const work = workHit._source
  const concepts = work.concepts.map((concept, index) => {
    return {
      name: concept,
      id: work.concept_ids[index],
    }
  })

  const contributors = work.contributors.map((contributor, index) => {
    return {
      name: contributor,
      id: work.contributor_ids[index],
    }
  })

  return {
    type: 'work',
    id: workHit._id,
    contributors: contributors,
    concepts: concepts,
    description: work.description,
    notes: work.notes,
    title: work.title,
  }
}
const index = process.env.ELASTIC_WORKS_INDEX as string

export function getWorks(client: Client, ids: string[]): Promise<Work[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: WorkHit) => {
      return parseWork(doc)
    })
  })
}

export async function searchWorks(
  client: Client,
  searchTerms: string
): Promise<Work[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  const results = response.body.hits.hits.map((doc: WorkHit) => {
    return parseWork(doc)
  })
  return JSON.parse(JSON.stringify(results))
}

export async function countWorks(
  client: Client,
  searchTerms: string
): Promise<number> {
  const response = await client.count({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  return response.body.count
}
