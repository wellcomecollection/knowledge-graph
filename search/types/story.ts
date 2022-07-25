export type StorySource = {
  contributors: string[]
  contributor_ids: string[]
  concepts: string[]
  concept_ids: string[]
  concept_variants: string[][]
  published: Date
  standfirst: string
  title: string
  wikidata_id: string | null
  type: string
}

export type StoryHit = {
  _id: string
  _score: string
  _source: StorySource
}

export type Story = {
  id: string
  type: string
  contributors: {
    id: string
    label: string
  }[]
  concepts: {
    id: string
    label: string
  }[]
  published: Date
  standfirst: string
  title: string
  wikidata_id: string | null
}
