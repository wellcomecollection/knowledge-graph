export type WorkSource = {
  contributors: string[]
  contributor_ids: string[]
  concepts: string[]
  concept_ids: string[]
  concept_variants: string[][]
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wikidata_id: string
  type: string
}

export type WorkHit = {
  _id: string
  _score: string
  _source: WorkSource
}

export type Work = {
  id: string
  type: string
  contributors: {
    id: string
    name: string
  }[]
  concepts: {
    id: string
    name: string
    variants: string[]
  }[]
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wikidata_id: string
}

export type ConceptSource = {
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  works: string[]
  work_ids: string[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
  type: string
}

export type ConceptHit = {
  _id: string
  _score: string
  _source: ConceptSource
}

export type Concept = {
  id: string
  type: string
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  works: {
    name: string
    id: string
  }[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}
