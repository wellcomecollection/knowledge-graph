export type WorkSource = {
  contributors: string[]
  contributor_ids: string[]
  concepts: string[]
  concept_ids: string[]
  concept_types: string[]
  concept_original_labels: string[]
  concept_variants: string[][]
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
  concepts: {
    id: string
    originalLabel: string
    label: string
    type: string
  }[]
  description: string
  notes: string
  title: string
  published: string[]
}
