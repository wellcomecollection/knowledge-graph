export type ConceptSource = {
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  works: string[]
  work_ids: string[]
  stories: string[]
  story_ids: string[]
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
  stories: {
    name: string
    id: string
  }[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}
