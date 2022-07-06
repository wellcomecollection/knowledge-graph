import Card, { CardProps } from './card'

import { FC } from 'react'

type Props = {
  title: string
  cards: CardProps[]
}

const CardBlock: FC<Props> = ({ title, cards }) => {
  return (
    <div className="mx-auto px-5 lg:w-3/4">
      <h1 className="">{title}</h1>
      <ul className="grid grid-cols-1 gap-3 pt-4 lg:grid-cols-3">
        {cards.map((card) => {
          return (
            <li key={card.title}>
              <Card
                imageURL={card.imageURL}
                imageAlt={card.imageAlt}
                title={card.title}
                description={card.description}
                URL={card.URL}
                type={card.type}
              />
            </li>
          )
        })}
      </ul>
    </div>
  )
}
export default CardBlock
