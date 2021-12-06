import {
  Concept,
  SourceConcept,
  SourceStory,
  Story,
} from '../types/elasticsearch'

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

export function parseConcept(concept: SourceConcept): Concept {
  const splitStoryTitles = concept.stories.split('<BREAK>')
  const splitStoryIds = concept.story_ids.split('<BREAK>')
  const stories = splitStoryTitles.map((storyTitle, index) => {
    return {
      name: storyTitle,
      id: splitStoryIds[index],
    }
  })
  return {
    lcsh_id: concept.lcsh_id,
    lcsh_preferred_name: concept.lcsh_preferred_name,
    mesh_description: concept.mesh_description,
    mesh_id: concept.mesh_id,
    mesh_preferred_name: concept.mesh_preferred_name,
    name: concept.name,
    stories,
    variants: concept.variants.split('<BREAK>'),
    wikidata_description: concept.wikidata_description,
    wikidata_id: concept.wikidata_id,
    wikidata_preferred_name: concept.wikidata_preferred_name,
  }
}
export function parseStory(story: SourceStory): Story {
  const splitConcepts = story.concepts.split('<BREAK>')
  const splitConceptIds = story.concept_ids.split('<BREAK>')
  const splitConceptVariants = story.concept_variants.split('<BREAK>')
  const concepts = splitConcepts.map((concept, index) => {
    return {
      name: concept,
      id: splitConceptIds[index],
      variants: splitConceptVariants[index].split('<SEP>'),
    }
  })

  return {
    contributors: story.contributors.split('<BREAK>'),
    concepts: concepts,
    fulltext: story.fulltext,
    published: new Date(story.published),
    standfirst: story.standfirst,
    title: story.title,
    wikidata_id: story.wikidata_id,
  }
}
