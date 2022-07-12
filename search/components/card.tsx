import { FC } from 'react'

const cardTypes = ['story', 'exhibition', 'event'] as const
type CardType = typeof cardTypes[number]

export type CardProps = {
  imageURL: string
  imageAlt: string
  title: string
  description: string
  URL: string
  type: CardType
}

const Card: FC<CardProps> = ({ imageURL, title, description, URL, type }) => {
  return (
    <div className="overflow-hidden rounded-lg bg-paper-3">
      <a href={URL} className="no-underline">
        <div className="relative">
          <img src={imageURL} alt={imageURL} />
          <div className="absolute bottom-0 left-0 bg-yellow py-1 px-3 text-sm">
            {type}
          </div>
        </div>
        <div className="h-24 py-2 px-3">
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
      </a>
    </div>
  )
}
export default Card
