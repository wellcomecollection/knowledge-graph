export type WhatsOnSource = {
  title: string
  description: string
  end_date: Date
  start_date: Date
  image_url: string
  image_alt: string
  format: string
}

export type WhatsOnHit = {
  _id: string
  _score: string
  _source: WhatsOnSource
}

export type WhatsOn = {
  id: string
  title: string
  description: string
  end_date: Date
  start_date: Date
  image_url: string
  image_alt: string
  format: string
}
