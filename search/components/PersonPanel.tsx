import { FC } from 'react'
import Link from 'next/link'
import { Person } from '../types/elasticsearch'

type Props = { person: Person }
const PersonPanel: FC<Props> = ({ person }) => {
  const title = person.wikidata_preferred_name || person.name
  const description = person.wikidata_description || null

  return (
    <div className="pt-5">
      <div className="bg-blue-800 py-3 px-4 text-white rounded-md ">
        <div>
          <div className="text-2xl font-semibold">{title}</div>
          <div className="text-sm md:w-3/4">{description}</div>
        </div>
        <div className="pt-5 pb-3">
          <Link href={`/people/${person.id}`}>
            <a className="no-underline px-3 py-2 rounded border-2 border-white text-sm">
              Find out more →
            </a>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default PersonPanel
