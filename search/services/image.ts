import { Image, ImageSource } from '../types/image'

import { Client } from '@elastic/elasticsearch'
import { URLSearchParams } from 'url'
import { capitalise } from '../components/results'
import { getPerson } from './person'
import { getSubject } from './subject'

export function parseImage(imageSource: ImageSource): Image {
  return {
    id: imageSource.id,
    url: imageSource.thumbnail.url.replace(
      'info.json',
      'full/,400/0/default.jpg'
    ),
    title: imageSource.source.title,
  }
}

export async function searchImages(
  client: Client,
  searchTerms: string,
  n: number
): Promise<Image[]> {
  const params = new URLSearchParams({
    query: encodeURIComponent(searchTerms),
    pageSize: n.toString(),
  })
  const response = await fetch(
    `https://api.wellcomecollection.org/catalogue/v2/images?${params}`
  ).then((res) => res.json())
  const results = response.results.map((doc: ImageSource) => {
    return parseImage(doc)
  })
  return JSON.parse(JSON.stringify(results))
}

export async function countImages(searchTerms: string): Promise<number> {
  const params = new URLSearchParams({ query: encodeURIComponent(searchTerms) })
  const response = await fetch(
    `https://api.wellcomecollection.org/catalogue/v2/images?${params}`
  ).then((res) => res.json())
  return response.totalResults
}

export async function filterImages(
  client: Client,
  subject?: string,
  person?: string
) {
  const label = subject
    ? (await getSubject(client, subject)).label
    : person
    ? (await getPerson(client, person)).label
    : ''
  const capitalisedLabel = capitalise(label)
  const url = `https://api.wellcomecollection.org/catalogue/v2/images?source.subjects.label=${capitalisedLabel}`
  const imageResponse = await fetch(url).then((res) => res.json())
  const results = imageResponse.results.map((image: ImageSource) => {
    return {
      id: image.source.id,
      url: image.thumbnail.url.replace('info.json', 'full/400,/0/default.jpg'),
      title: image.source.title,
    }
  }) as Image[]

  return JSON.parse(
    JSON.stringify({ results, resultCount: imageResponse.totalResults })
  )
}
