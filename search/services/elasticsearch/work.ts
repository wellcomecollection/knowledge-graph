import { Work, WorkHit } from '../../types/work'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/works.json'
import { formatQuery } from '.'

const index = process.env.ELASTIC_WORKS_INDEX as string

export function parseWork(workHit: WorkHit): Work {
  const work = workHit._source
  const concepts = work.concepts.map((concept, index) => {
    return {
      label: concept,
      id: work.concept_ids[index],
      type: work.concept_types[index],
      originalLabel: work.concept_original_labels[index],
    }
  })

  const contributors = work.contributors.map((contributor, index) => {
    return {
      label: contributor,
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
    published: work.published,
  }
}

export function getWorks(client: Client, ids: string[]): Promise<Work[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: WorkHit) => {
      return parseWork(doc)
    })
  })
}

export function getWork(client: Client, id: string): Promise<Work> {
  const work = client.get({ index, id }).then((response) => {
    return parseWork(response.body as WorkHit)
  })
  return work
}

export async function searchWorks(
  client: Client,
  searchTerms: string,
  n: number
): Promise<Work[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
    size: n,
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

export async function filterWorks(
  client: Client,
  subject?: string,
  person?: string
): Promise<Work[]> {
  const field = subject ? 'concept_ids' : person ? 'contributor_ids' : null
  const value = subject ? subject : person ? person : null
  const response = await client.search({
    index,
    body: `{"query": {"bool": {"must": [{"match": {"${field}": "${value}"}}]}}}`,
  })
  const results = response.body.hits.hits.map((doc: WorkHit) => {
    return parseWork(doc)
  })
  const resultCount = response.body.hits.total.value
  return JSON.parse(JSON.stringify({ results, resultCount }))
}
