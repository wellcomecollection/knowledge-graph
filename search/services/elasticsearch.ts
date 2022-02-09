import { Concept, ConceptHit, Work, WorkHit } from '../types/elasticsearch'

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
  return {
    type: concept.type,
    id: conceptHit._id,
    lcsh_id: concept.lcsh_id,
    lcsh_preferred_name: concept.lcsh_preferred_name,
    mesh_description: concept.mesh_description,
    mesh_id: concept.mesh_id,
    mesh_preferred_name: concept.mesh_preferred_name,
    name: concept.name,
    works,
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
      variants: work.concept_variants[index],
    }
  })
  const contributors = work.contributors.map((contributor, index) => {
    return {
      name: contributor,
      id: work.contributor_ids[index],
    }
  })

  return {
    type: work.type,
    id: workHit._id,
    contributors: contributors,
    concepts: concepts,
    fulltext: work.fulltext,
    published: new Date(work.published),
    standfirst: work.standfirst,
    title: work.title,
    wikidata_id: work.wikidata_id,
  }
}
