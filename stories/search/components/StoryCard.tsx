import { FC } from 'react'

type Props = {
  title: string
  id: string
  standfirst: string
  imageURL?: string
}
const StoryCard: FC<Props> = ({ title, id, standfirst, imageURL }) => {
  const url = `https://wellcomecollection.org/articles/${id}`
  return (
    <a className="no-underline" href={url}>
      <div className="h-full bg-gray-200 rounded">
        <div className="py-2 px-3">
          <h3>{title}</h3>
          <p className="text-xs">{standfirst}</p>
        </div>
      </div>
    </a>
  )
}

export default StoryCard
