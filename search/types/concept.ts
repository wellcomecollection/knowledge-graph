export type ConceptSource = {
  lc_names_id?: string
  lc_names_preferred_label?: string
  lc_subjects_id?: string
  lc_subjects_preferred_label?: string
  mesh_description?: string
  mesh_id?: string
  mesh_preferred_label?: string
  label?: string
  preferred_label?: string
  works: string[]
  work_ids: string[]
  neighbour_ids: string[]
  neighbour_labels: string[]
  stories: string[]
  story_contribution_ids: string[]
  story_contributions: string[]
  story_ids: string[]
  type?: string
  variants: string[]
  wikidata_description?: string
  wikidata_id?: string
  wikidata_preferred_label?: string
  work_contribution_ids: string[]
  work_contributions: string[]
}

export type ConceptHit = {
  _id: string
  _score: string
  _source: ConceptSource
}

export type Concept = {
  id: string
  lc_names_id?: string
  lc_names_preferred_label?: string
  lc_subjects_id?: string
  lc_subjects_preferred_label?: string
  mesh_description?: string
  mesh_id?: string
  mesh_preferred_label?: string
  label?: string
  preferred_label?: string
  works: {
    title: string
    id: string
  }[]
  neighbours: {
    id: string
    label: string
  }[]
  type?: string
  stories: {
    title: string
    id: string
  }[]
  story_contributions: {
    title: string
    id: string
  }[]
  variants: string[]
  work_contributions: {
    title: string
    id: string
  }[]
  wikidata_description?: string
  wikidata_id?: string
  wikidata_preferred_label?: string
}
