import { Person, PersonHit } from '../types/person'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../data/queries/concepts-loose.json'
import { formatQuery } from '.'

const index = process.env.ELASTIC_PEOPLE_INDEX as string
export function parsePerson(personHit: PersonHit): Person {
  const person = personHit._source
  const works = person.works.map((workTitle, index) => {
    return {
      title: workTitle,
      id: person.work_ids[index],
    }
  })
  const stories = person.stories.map((storyTitle, index) => {
    return {
      title: storyTitle,
      id: person.story_ids[index],
    }
  })
  const work_contributions = person.work_contributions
    ? person.work_contributions.map((workTitle, index) => {
        return {
          title: workTitle,
          id: person.work_contribution_ids[index],
        }
      })
    : []
  const story_contributions = person.story_contributions
    ? person.story_contributions.map((storyTitle, index) => {
        return {
          title: storyTitle,
          id: person.story_contribution_ids[index],
        }
      })
    : []

  return {
    ...person,
    id: personHit._id,
    works,
    stories,
    work_contributions,
    story_contributions,
  }
}

export async function searchPeople(
  client: Client,
  searchTerms: string
): Promise<Person[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  const results = response.body.hits.hits.map((doc: PersonHit) => {
    return parsePerson(doc)
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
      return parsePerson(doc)
    })
  })
}

export function getPerson(client: Client, id: string): Promise<Person> {
  return client.get({ index, id }).then((response) => {
    return parsePerson(response.body as PersonHit) as Person
  })
}
