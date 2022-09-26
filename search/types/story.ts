export type StorySource = {
  contributors: string[]
  contributor_ids: string[]
  subjects: string[]
  subject_ids: string[]
  subject_variants: string[][]
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
  subjects: {
    id: string
    label: string
  }[]
  published: Date
  standfirst: string
  title: string
  wikidata_id: string | null
}
