export type Story = {
  title: string
  published: Date
  contributors: string
  wikidata_id: string
  wellcome_id: string
  fulltext: string
  standfirst: string
}

export type Hit = {
  _id: string
  _score: string
  _source: Story
}
