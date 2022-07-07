import { Concept, ConceptHit } from '../../types/concept'
import { Person, PersonHit, PersonSource } from '../../types/person'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/concepts-loose.json'
import { formatQuery } from '.'
import { parseConcept } from './subject'

const index = process.env.ELASTIC_PEOPLE_INDEX as string

export async function searchPeople(
  client: Client,
  searchTerms: string
): Promise<Concept[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  const results = response.body.hits.hits.map((doc: ConceptHit) => {
    return parseConcept(doc)
  })
  return JSON.parse(JSON.stringify(results))
}

export async function countPeople(
  client: Client,
  searchTerms: string
): Promise<number> {
  const response = await client.count({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  return response.body.count
}

export function getPeople(client: Client, ids: string[]): Promise<Person[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: PersonHit) => {
      return parseConcept(doc)
    })
  })
}

export function getPerson(client: Client, id: string): Promise<Person> {
  return client.get({ index, id }).then((response) => {
    return parseConcept(response.body as PersonHit) as Person
  })
}
