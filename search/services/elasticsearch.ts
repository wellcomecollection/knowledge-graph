import { Concept, ConceptHit } from '../types/concept'
import { Story, StoryHit } from '../types/story'
import { Work, WorkHit } from '../types/work'

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
  const works = concept.works.map((workTitle, index) => {
    return {
      name: workTitle,
      id: concept.work_ids[index],
    }
  })
  const stories = concept.stories.map((storyTitle, index) => {
    return {
      name: storyTitle,
      id: concept.story_ids[index],
    }
  })

  return {
    type: concept.type,
    id: conceptHit._id,
    lc_subjects_id: concept.lc_subjects_id,
    lc_subjects_preferred_name: concept.lc_subjects_preferred_name,
    lc_names_id: concept.lc_names_id,
    lc_names_preferred_name: concept.lc_names_preferred_name,
    mesh_description: concept.mesh_description,
    mesh_id: concept.mesh_id,
    mesh_preferred_name: concept.mesh_preferred_name,
    name: concept.name,
    works,
    stories,
    variants: concept.variants,
    wikidata_description: concept.wikidata_description,
    wikidata_id: concept.wikidata_id,
    wikidata_preferred_name: concept.wikidata_preferred_name,
  }
}

export function parseWork(workHit: WorkHit): Work {
  const work = workHit._source
  const concepts = work.concepts.map((concept, index) => {
    return {
      name: concept,
      id: work.concept_ids[index],
    }
  })

  const contributors = work.contributors.map((contributor, index) => {
    return {
      name: contributor,
      id: work.contributor_ids[index],
    }
  })

  return {
    type: 'work',
    id: workHit._id,
    contributors: contributors,
    concepts: concepts,
    description: work.description,
    notes: work.notes,
    title: work.title,
  }
}

export function parseStory(storyHit: StoryHit): Story {
  const story = storyHit._source
  const concepts = story.concepts.map((concept, index) => {
    return {
      name: concept,
      id: story.concept_ids[index],
    }
  })
  const contributors = story.contributors.map((contributor, index) => {
    return {
      name: contributor,
      id: story.contributor_ids[index],
    }
  })

  return {
    type: 'story',
    id: storyHit._id,
    contributors: contributors,
    concepts: concepts,
    published: new Date(story.published),
    standfirst: story.standfirst,
    title: story.title,
    wikidata_id: story.wikidata_id,
  }
}
