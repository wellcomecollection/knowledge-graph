import { WhatsOn, WhatsOnHit } from '../../types/whats-on'

import { Client } from '@elastic/elasticsearch'
import blankQuery from '../../data/queries/whats-on.json'
import { formatQuery } from '.'

export function parseWhatsOn(whatsOnHit: WhatsOnHit): WhatsOn {
  const { _source } = whatsOnHit
  return {
    id: whatsOnHit._id,
    title: _source.title,
    description: _source.description,
    end_date: _source.end_date,
    start_date: _source.start_date,
    image_url: _source.image_url,
    image_alt: _source.image_alt,
    format: _source.format,
  }
}

const index = process.env.ELASTIC_WHATS_ON_INDEX as string

export function getWhatsOns(client: Client, ids: string[]): Promise<WhatsOn[]> {
  return client.mget({ index, body: { ids } }).then((response) => {
    return response.body.docs.map((doc: WhatsOnHit) => {
      return parseWhatsOn(doc)
    })
  })
}

export function getWhatsOn(client: Client, id: string): Promise<WhatsOn> {
  return client.get({ index, id }).then((response) => {
    return parseWhatsOn(response.body as WhatsOnHit)
  })
}

export async function searchWhatsOn(
  client: Client,
  searchTerms: string,
  n: number
): Promise<WhatsOn[]> {
  const response = await client.search({
    index,
    body: formatQuery(blankQuery, searchTerms),
    size: n,
  })
  const results = response.body.hits.hits.map((doc: WhatsOnHit) => {
    return parseWhatsOn(doc)
  })

  return JSON.parse(JSON.stringify(results))
}

export async function countWhatsOn(
  client: Client,
  searchTerms: string
): Promise<number> {
  const response = await client.count({
    index,
    body: formatQuery(blankQuery, searchTerms),
  })
  return response.body.count
}
