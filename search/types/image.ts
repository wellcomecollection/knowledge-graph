export type ImageSource = {
  id: string
  thumbnail: { url: string }
  source: {
    id: string
    title: string
    type: string
  }
}

export type Image = {
  id: string
  url: string
  title: string
}
