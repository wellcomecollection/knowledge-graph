import { SubjectSource } from './subject'

export type PersonSource = SubjectSource & {
  dates?: string[]
  date_labels?: string[]
}

export type PersonHit = {
  _id: string
  _score: string
  _source: PersonSource
}

export type Person = {
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
  type: string
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
  dates: {
    value: string
    label: string
  }[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_label: string
}
