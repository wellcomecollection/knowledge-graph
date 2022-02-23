import { FC } from 'react'

type Props = {
  type: string
  title: string
  id: string
  color: string
  contributors?: string[]
  imageURL?: string
}
const Card: FC<Props> = ({
  type,
  title,
  id,
  contributors,
  color,
  imageURL,
}) => {
  const url = `https://wellcomecollection.org/${
    type == 'work' ? 'works' : 'articles'
  }/${id}`
  const croppedTitle =
    title.length > 50 ? title.substring(0, 50) + '...' : title
  return (
    <a className="no-underline" href={url}>
      <div className={`h-full bg-${color}`}>
        {imageURL ? (
          <div className="relative pb-2/3">
            <img
              src={imageURL}
              alt="a very image"
              className="absolute h-full w-full object-cover"
            />
          </div>
        ) : null}
        <div className="px-3 pt-2 pb-8 leading-snug">
          <h4>{croppedTitle}</h4>
          {contributors ? (
            <p className="text-sm capitalize">{contributors.join(', ')}</p>
          ) : null}
        </div>
      </div>
    </a>
  )
}

export default Card
