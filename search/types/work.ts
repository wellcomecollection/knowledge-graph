export type WorkSource = {
  contributors: string[]
  contributor_ids: string[]
  subjects: string[]
  subject_parent_labels: string[]
  subject_ids: string[]
  subject_types: string[]
  subject_variants: string[][]
  subject_preferred_label_sources: string
  description: string
  notes: string
  title: string
  type: string
  published: string[]
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
    label: string
  }[]
  subjects: {
    id: string
    parent_label: string
    label: string
    type: string
    source: string
  }[]
  description: string
  notes: string
  title: string
  published: string[]
}
