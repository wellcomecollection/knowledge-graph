export type Doc = {
  Title: string
  URL: string
  'Date published': number
  Author: string
  'Images by': string | null
  Type: string
  'Part of': string | null
  Keywords: string
  Notes: string
  Quarter: string
  'Relates to': string
  'Wikidata ID': string
  id: string
  fulltext: string
  standfirst: string
}

export type Hit = {
  _id: string
  _score: string
  _source: Doc
}
