import { countImages, searchImages } from './image'
import { countPeople, searchPeople } from './person'
import { countStories, searchStories } from './story'
import { countSubjects, searchSubjects } from './subject'
import { countWhatsOn, searchWhatsOn } from './whats-on'
import { countWorks, searchWorks } from './work'

import { Client } from '@elastic/elasticsearch'
import { Image } from '../../types/image'
import { Story } from '../../types/story'
import { Tab } from '../../components/tabs'
import { WhatsOn } from '../../types/whats-on'
import { Work } from '../../types/work'

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
  images: searchImages,
  stories: searchStories,
  'whats-on': searchWhatsOn,
  works: searchWorks,
}

export async function search(
  index: string,
  searchTerms: string,
  client: Client,
  n: number
) {
  return await searchServices[index](client, searchTerms, n)
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
