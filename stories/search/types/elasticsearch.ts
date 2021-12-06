export type SourceStory = {
  contributors: string[]
  concepts: string[]
  concept_ids: string[]
  concept_variants: string[][]
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wikidata_id: string
}

export type StoryHit = {
  _id: string
  _score: string
  _source: SourceStory
}

export type Story = {
  id: string
  contributors: string[]
  concepts: {
    name: string
    id: string
    variants: string[]
  }[]
  fulltext: string
  published: Date
  standfirst: string
  title: string
  wikidata_id: string
}

export type SourceConcept = {
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  stories: string[]
  story_ids: string[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}

export type ConceptHit = {
  _id: string
  _score: string
  _source: SourceConcept
}

export type Concept = {
  id: string
  lcsh_id: string
  lcsh_preferred_name: string
  mesh_description: string
  mesh_id: string
  mesh_preferred_name: string
  name: string
  stories: {
    name: string
    id: string
  }[]
  variants: string[]
  wikidata_description: string
  wikidata_id: string
  wikidata_preferred_name: string
}
