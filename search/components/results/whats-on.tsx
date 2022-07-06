import { FC } from 'react'
import { WhatsOn } from '../../types/whats-on'
import { formatDate } from '.'

type WhatsOnResultProps = {
  result: WhatsOn
}
export const WhatsOnResult: FC<WhatsOnResultProps> = ({ result }) => {
  return (
    <li key={result.title}>
      <div className="h-full bg-paper-3">
        <div className="relative pb-2/3">
          <img
            src={result.image_url}
            alt={result.image_url}
            className="absolute h-full w-full object-cover"
          />
          <div className="absolute bottom-0 left-0 bg-yellow py-1 px-2 text-sm font-semibold capitalize">
            {result.format}
          </div>
        </div>
        <div className="h-full px-3 pt-2 pb-4">
          <h3>{result.title}</h3>
          <p className="text-sm">
            {formatDate(result.start_date)} - {formatDate(result.end_date)}
          </p>
        </div>
      </div>
    </li>
  )
}

type WhatsOnResultsProps = {
  results: WhatsOn[]
}
const WhatsOnResults: FC<WhatsOnResultsProps> = ({ results }) => {
  return (
    <ul className="grid h-auto grid-cols-1 gap-3 pt-4 xl:grid-cols-3">
      {results.map((result) => {
        return <WhatsOnResult result={result} key={result.id} />
      })}
    </ul>
  )
}
export default WhatsOnResults
