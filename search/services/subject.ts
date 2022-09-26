import { Person, PersonHit } from '../types/person'
import { Subject, SubjectHit } from '../types/subject'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../data/queries/concepts-loose.json'
import { formatQuery } from '.'

export function parseSubject(subjectHit: SubjectHit): Subject {
  const subject = subjectHit._source
  const works = subject.works.map((workTitle, index) => {
    return {
      title: workTitle,
      id: subject.work_ids[index],
    }
  })
  const stories = subject.stories.map((storyTitle, index) => {
    return {
      title: storyTitle,
      id: subject.story_ids[index],
    }
  })
  const work_contributions = subject.work_contributions
    ? subject.work_contributions.map((workTitle, index) => {
        return {
          title: workTitle,
          id: subject.work_contribution_ids[index],
        }
      })
    : []
  const story_contributions = subject.story_contributions
    ? subject.story_contributions.map((storyTitle, index) => {
        return {
          title: storyTitle,
          id: subject.story_contribution_ids[index],
        }
      })
    : []
  const neighbours = subject.neighbour_ids.map((id, index) => {
    return {
      id,
      label: subject.neighbour_labels[index],
    }
  })

  return {
    ...subject,
    id: subjectHit._id,
    neighbours,
    works,
    stories,
    work_contributions,
    story_contributions,
  }
}
const index = process.env.ELASTIC_SUBJECTS_INDEX as string

export function getSubjects(client: Client, ids: string[]): Promise<Subject[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: SubjectHit) => {
      return parseSubject(doc)
    })
  })
}

export function getSubject(client: Client, id: string): Promise<Subject> {
  return client.get({ index, id }).then((response) => {
    return parseSubject(response.body as SubjectHit)
  })
}

export async function searchSubjects(
  client: Client,
  searchTerms: string
): Promise<Subject[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  const results = response.body.hits.hits.map((doc: SubjectHit) => {
    return parseSubject(doc)
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
