export type Story = {
  contributors: string
  concepts: string
  concept_ids: string
  concept_variants: string
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wikidata_id: string
}

export type Concept = {
  name: string
  description: string
  variants: string
  stories: string
  story_ids: string
}

export type Hit = {
  _id: string
  _score: string
  _source: Story
}
