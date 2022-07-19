import { Concept, ConceptHit } from '../../types/concept'
import { Person, PersonHit } from '../../types/person'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/concepts-loose.json'
import { formatQuery } from '.'

export function parseConcept(
  conceptHit: ConceptHit | PersonHit
): Concept | Person {
  const concept = conceptHit._source
  const works = concept.works.map((workTitle, index) => {
    return {
      title: workTitle,
      id: concept.work_ids[index],
    }
  })
  const stories = concept.stories.map((storyTitle, index) => {
    return {
      title: storyTitle,
      id: concept.story_ids[index],
    }
  })
  const work_contributions = concept.work_contributions
    ? concept.work_contributions.map((workTitle, index) => {
        return {
          title: workTitle,
          id: concept.work_contribution_ids[index],
        }
      })
    : []
  const story_contributions = concept.story_contributions
    ? concept.story_contributions.map((storyTitle, index) => {
        return {
          title: storyTitle,
          id: concept.story_contribution_ids[index],
        }
      })
    : []
  const neighbours = concept.neighbour_ids.map((id, index) => {
    return {
      id,
      name: concept.neighbour_names[index],
    }
  })

  return {
    ...concept,
    id: conceptHit._id,
    neighbours,
    works,
    stories,
    work_contributions,
    story_contributions,
  }
}
const index = process.env.ELASTIC_SUBJECTS_INDEX as string

export function getSubjects(client: Client, ids: string[]): Promise<Concept[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: ConceptHit) => {
      return parseConcept(doc)
    })
  })
}

export function getSubject(client: Client, id: string): Promise<Concept> {
  return client.get({ index, id }).then((response) => {
    return parseConcept(response.body as ConceptHit)
  })
}

export async function searchSubjects(
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

export async function countSubjects(
  client: Client,
  searchTerms: string
): Promise<number> {
  const response = await client.count({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  return response.body.count
}
