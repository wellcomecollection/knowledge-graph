import { FC } from 'react'

type Props = {
  type: string
  title: string
  id: string
  description?: string
  imageURL?: string
}
const Card: FC<Props> = ({ type, title, id, description, imageURL }) => {
  const url = `https://wellcomecollection.org/${
    type == 'work' ? 'works' : 'articles'
  }/${id}`
  return (
    <a className="no-underline" href={url}>
      <div className="h-full bg-red">
        <div className="py-2 px-3">
          <h3 className="leading-snug">{title}</h3>
          {description ? <p className="pt-1 text-xs">{description}</p> : null}
        </div>
      </div>
    </a>
  )
}

export default Card
