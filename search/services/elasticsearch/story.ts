import { Story, StoryHit } from '../../types/story'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/stories.json'
import { formatQuery } from '.'

const index = process.env.ELASTIC_STORIES_INDEX as string

export function parseStory(storyHit: StoryHit): Story {
  const story = storyHit._source
  const concepts = story.concepts.map((concept, index) => {
    return {
      label: concept,
      id: story.concept_ids[index],
    }
  })
  const contributors = story.contributors.map((contributor, index) => {
    return {
      label: contributor,
      id: story.contributor_ids[index],
    }
  })

  return {
    type: 'story',
    id: storyHit._id,
    contributors: contributors,
    concepts: concepts,
    published: story.published,
    standfirst: story.standfirst,
    title: story.title,
    wikidata_id: story.wikidata_id ? story.wikidata_id : null,
  }
}

export function getStories(client: Client, ids: string[]): Promise<Story> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: StoryHit) => {
      return parseStory(doc)
    })
  })
}

export function getStory(client: Client, id: string): Promise<Story> {
  return client.get({ index, id }).then((response) => {
    return parseStory(response.body as StoryHit)
  })
}

export function getRecentStories(client: Client, n: number): Promise<Story> {
  return client
    .search({
      index,
      body: {
        query: {
          match_all: {},
        },
        sort: [{ published: { order: 'desc' } }],
        size: n,
      },
    })
    .then((response) => {
      return response.body.hits.hits.map((doc: StoryHit) => {
        return parseStory(doc)
      })
    })
}

export async function searchStories(
  client: Client,
  searchTerms: string,
  n: number
): Promise<Story[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
    size: n,
  })
  const results = response.body.hits.hits.map((doc: StoryHit) => {
    return parseStory(doc)
  })
  return JSON.parse(JSON.stringify(results))
}

export async function countStories(
  client: Client,
  searchTerms: string
): Promise<number> {
  const response = await client.count({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  return response.body.count
}

export async function filterStories(
  client: Client,
  subject?: string,
  person?: string
): Promise<Story[]> {
  const field = subject ? 'concept_ids' : person ? 'contributor_ids' : null
  const value = subject ? subject : person ? person : null
  const response = await client.search({
    index,
    body: `{"query": {"bool": {"must": [{"match": {"${field}": "${value}"}}]}}}`,
  })
  const results = response.body.hits.hits.map((doc: StoryHit) => {
    return parseStory(doc)
  })
  const resultCount = response.body.hits.total.value
  return JSON.parse(JSON.stringify({ results, resultCount }))
}
