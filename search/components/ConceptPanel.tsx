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
    <div className={`flex bg-${color} py-3 px-4 text-white`}>
      <div className="my-auto flex-auto">
        <h2 className="titlecase text-2xl font-semibold">{title}</h2>
        <p className="mr-5 text-sm">{description}</p>
      </div>
      <div className="my-auto flex-none">
        <Link href={`/concepts/${concept.id}`}>
          <a className="border-2 border-white px-3 py-2 text-sm no-underline">
            Find out more →
          </a>
        </Link>
      </div>
    </div>
  )
}

export default ConceptPanel
