export type ConceptSource = {
  lc_subjects_id: string
  lc_subjects_preferred_name: string
  lc_names_id: string
  lc_names_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  preferred_name: string
  works: string[]
  work_ids: string[]
  stories: string[]
  story_ids: string[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
  type: string
  work_contributions: string[]
  work_contribution_ids: string[]
  story_contributions: string[]
  story_contribution_ids: string[]
}

export type ConceptHit = {
  _id: string
  _score: string
  _source: ConceptSource
}

export type Concept = {
  id: string
  type: string
  lc_subjects_id: string
  lc_subjects_preferred_name: string
  lc_names_id: string
  lc_names_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  preferred_name: string
  works: {
    name: string
    id: string
  }[]
  stories: {
    name: string
    id: string
  }[]
  work_contributions: {
    name: string
    id: string
  }[]
  story_contributions: {
    name: string
    id: string
  }[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}
