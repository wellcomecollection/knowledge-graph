import { ConceptSource } from './concept'

export type PersonSource = ConceptSource & {
  dates: string[]
  date_labels: string[]
}

export type PersonHit = {
  _id: string
  _score: string
  _source: PersonSource
}

export type Person = {
  id: string
  lc_names_id: string
  lc_names_preferred_name: string
  lc_subjects_id: string
  lc_subjects_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  preferred_name: string
  works: {
    name: string
    id: string
  }[]
  neighbours: {
    id: string
    name: string
  }[]
  type: string
  stories: {
    name: string
    id: string
  }[]
  story_contributions: {
    name: string
    id: string
  }[]
  variants: string[]
  work_contributions: {
    name: string
    id: string
  }[]
  dates: {
    value: string
    label: string
  }[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}
