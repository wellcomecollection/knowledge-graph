import { Concept } from '../types/concept'
import { FC } from 'react'
import Link from 'next/link'

type Props = { concept: Concept; color: string }
const ConceptPanel: FC<Props> = ({ concept, color }) => {
  const title =
    concept.wikidata_preferred_name ||
    concept.mesh_preferred_name ||
    concept.lcsh_preferred_name ||
    concept.name
  const description = concept.wikidata_description || concept.mesh_description

  return (
    <div className="pt-5">
      <div className={`bg-${color}-700 py-3 px-4 text-white rounded-md `}>
        <div>
          <div className="text-2xl font-semibold">{title}</div>
          <div className="text-sm md:w-3/4">{description}</div>
        </div>
        <div className="pt-5 pb-3">
          <Link href={`/concepts/${concept.id}`}>
            <a className="no-underline px-3 py-2 rounded border-2 border-white text-sm">
              Find out more →
            </a>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default ConceptPanel
