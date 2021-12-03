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
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  stories: string
  story_ids: string
  variants: string
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}

export type Hit = {
  _id: string
  _score: string
  _source: Story
}
