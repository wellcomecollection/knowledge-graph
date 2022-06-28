import { Image, ImageSource } from '../../types/image'

import { URLSearchParams } from 'url'

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
  client,
  searchTerms: string
): Promise<Image[]> {
  const params = new URLSearchParams({ query: encodeURIComponent(searchTerms) })
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
