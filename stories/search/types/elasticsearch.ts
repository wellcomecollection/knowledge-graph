export type Story = {
  contributors: string
  concepts: string
  concepts_variants: string
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wellcome_id: string
  wikidata_id: string
}
export type Concept = {
  id: string
  name: string
  description: string
  variants: string
  stories: string
}

export type Hit = {
  _id: string
  _score: string
  _source: Story
}
