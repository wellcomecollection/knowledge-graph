import { Slug, Tab, slugToTab } from '../../components/tabs'
import { countImages, searchImages } from './image'
import { countStories, searchStories } from './story'
import { countWhatsOn, searchWhatsOn } from './whats-on'
import { countWorks, searchWorks } from './work'

import { Client } from '@elastic/elasticsearch'

const { ELASTIC_PASSWORD, ELASTIC_USERNAME, ELASTIC_CLOUD_ID } = process.env

let client: Client
export function getClient(): Client {
  client = new Client({
    cloud: {
      id: ELASTIC_CLOUD_ID!,
    },
    auth: {
      username: ELASTIC_USERNAME!,
      password: ELASTIC_PASSWORD!,
    },
  })
  return client
}

export function formatQuery(blankQuery: object, searchTerms: string): object {
  return {
    query: JSON.parse(
      JSON.stringify(blankQuery).replace(/{{query}}/g, searchTerms)
    ),
  }
}

export async function getResultCounts(
  client: Client,
  searchTerms: string
): Promise<{ [key in Tab]: number }> {
  return {
    Images: await countImages(searchTerms),
    Works: await countWorks(client, searchTerms),
    Stories: await countStories(client, searchTerms),
    "What's on": await countWhatsOn(client, searchTerms),
  }
}

const searchServices = {
  Images: searchImages,
  Works: searchWorks,
  Stories: searchStories,
  "What's on": searchWhatsOn,
}

export async function search(
  index: string,
  searchTerms: string,
  client: Client,
  n: number
) {
  const searchService = searchServices[slugToTab[index] as Tab]
  return await searchService(client, searchTerms, n)
}

export { getWorks, getWork, parseWork, searchWorks } from './work'
export { parseImage, searchImages } from './image'
export { searchPeople } from './person'
export { searchWhatsOn } from './whats-on'
export {
  getSubjects,
  getSubject,
  parseConcept,
  searchSubjects,
} from './subject'

export {
  getStories,
  getRecentStories,
  parseStory,
  searchStories,
} from './story'
