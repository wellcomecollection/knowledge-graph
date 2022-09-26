import { Tab, slugToTab } from '../components/tabs'
import { countImages, filterImages, searchImages } from './image'
import { countStories, filterStories, searchStories } from './story'
import { countWhatsOn, filterWhatsOn, searchWhatsOn } from './whats-on'
import { countWorks, filterWorks, searchWorks } from './work'

import { Client } from '@elastic/elasticsearch'

const {
  ELASTIC_CONCEPTS_PASSWORD,
  ELASTIC_CONCEPTS_USERNAME,
  ELASTIC_CONCEPTS_CLOUD_ID,
  ELASTIC_PIPELINE_CLOUD_ID,
  ELASTIC_PIPELINE_USERNAME,
  ELASTIC_PIPELINE_PASSWORD
} = process.env

let client: Client
export function getClient(): Client {
  client = new Client({
    cloud: {
      id: ELASTIC_CONCEPTS_CLOUD_ID!,
    },
    auth: {
      username: ELASTIC_CONCEPTS_USERNAME!,
      password: ELASTIC_CONCEPTS_PASSWORD!,
    },
  })
  return client
}

let pipelineClient: Client
export function getPipelineClient(): Client {
  client = new Client({
    cloud: {
      id: ELASTIC_PIPELINE_CLOUD_ID!,
    },
    auth: {
      username: ELASTIC_PIPELINE_USERNAME!,
      password: ELASTIC_PIPELINE_PASSWORD!,
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

const filterServices = {
  Images: filterImages,
  Works: filterWorks,
  Stories: filterStories,
  "What's on": filterWhatsOn,
}

export async function filter(
  client: Client,
  index: string,
  subject?: string,
  person?: string
) {
  const filterService = filterServices[slugToTab[index] as Tab]
  return await filterService(client, subject, person)
}

export { getWorks, getWork, parseWork, searchWorks } from './work'
export { parseImage, searchImages } from './image'
export { searchPeople, getPeople, getPerson, parsePerson } from './person'
export {
  searchWhatsOn,
  getWhatsOn,
  getWhatsOns,
  parseWhatsOn,
} from './whats-on'
export {
  getSubjects,
  getSubject,
  parseSubject,
  searchSubjects,
} from './subject'

export {
  getStories,
  getStory,
  getRecentStories,
  parseStory,
  searchStories,
} from './story'
