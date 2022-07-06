import { FC } from 'react'
import { WhatsOn } from '../../types/whats-on'
import { formatDate } from '.'

type Props = {
  results: WhatsOn[]
}
export const WhatsOnResult: FC<WhatsOn> = ({ whatsOn }) => {
  return (
    <li key={whatsOn.title}>
      <div className="h-full bg-paper-3">
        <div className="relative pb-2/3">
          <img
            src={whatsOn.image_url}
            alt={whatsOn.image_url}
            className="absolute h-full w-full object-cover"
          />
          <div className="absolute bottom-0 left-0 bg-yellow py-1 px-2 text-sm font-semibold capitalize">
            {whatsOn.format}
          </div>
        </div>
        <div className="h-full px-3 pt-2 pb-4">
          <h3>{whatsOn.title}</h3>
          <p className="text-sm">
            {formatDate(whatsOn.start_date)} - {formatDate(whatsOn.end_date)}
          </p>
        </div>
      </div>
    </li>
  )
}

const WhatsOnResults: FC<Props> = ({ results }) => {
  return (
    <ul className="grid h-auto grid-cols-1 gap-3 pt-4 xl:grid-cols-3">
      {results.map((whatsOn) => {
        return <WhatsOnResult whatsOn={whatsOn} key={whatsOn.title} />
      })}
    </ul>
  )
}
export default WhatsOnResults
