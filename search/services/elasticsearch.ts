import {
  Concept,
  ConceptHit,
  Person,
  PersonHit,
  Story,
  StoryHit,
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

export function parseConcept(conceptHit: ConceptHit): Concept {
  const concept = conceptHit._source
  const stories = concept.stories.map((storyTitle, index) => {
    return {
      name: storyTitle,
      id: concept.story_ids[index],
    }
  })
  return {
    id: conceptHit._id,
    lcsh_id: concept.lcsh_id,
    lcsh_preferred_name: concept.lcsh_preferred_name,
    mesh_description: concept.mesh_description,
    mesh_id: concept.mesh_id,
    mesh_preferred_name: concept.mesh_preferred_name,
    name: concept.name,
    stories,
    variants: concept.variants,
    wikidata_description: concept.wikidata_description,
    wikidata_id: concept.wikidata_id,
    wikidata_preferred_name: concept.wikidata_preferred_name,
  }
}

export function parsePerson(personHit: PersonHit): Person {
  const concept = personHit._source
  const stories = concept.stories.map((storyTitle, index) => {
    return {
      name: storyTitle,
      id: concept.story_ids[index],
    }
  })
  return {
    id: personHit._id,
    name: concept.name,
    stories,
    variants: concept.variants,
    wikidata_description: concept.wikidata_description,
    wikidata_id: concept.wikidata_id,
    wikidata_preferred_name: concept.wikidata_preferred_name,
  }
}

export function parseStory(storyHit: StoryHit): Story {
  const story = storyHit._source
  const concepts = story.concepts.map((concept, index) => {
    return {
      name: concept,
      id: story.concept_ids[index],
      variants: story.concept_variants[index],
    }
  })
  const contributors = story.contributors.map((contributor, index) => {
    return {
      name: contributor,
      id: story.contributor_ids[index],
    }
  })

  return {
    id: storyHit._id,
    contributors: contributors,
    concepts: concepts,
    fulltext: story.fulltext,
    published: new Date(story.published),
    standfirst: story.standfirst,
    title: story.title,
    wikidata_id: story.wikidata_id,
  }
}
