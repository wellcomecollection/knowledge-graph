export type WorkSource = {
  contributors: string[]
  contributor_ids: string[]
  concepts: string[]
  concept_ids: string[]
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
    name: string
  }[]
  concepts: {
    id: string
    name: string
  }[]
  description: string
  notes: string
  title: string
  published: string[]
}
