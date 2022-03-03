import { Concept } from '../types/concept'
import { FC } from 'react'
import Link from 'next/link'

type Props = { concept: Concept }
const ConceptPanel: FC<Props> = ({ concept }) => {
  const title = concept.preferred_name
  const description = concept.wikidata_description || concept.mesh_description

  return (
    <>
      <div
        className={` ${
          concept.type == 'concept' ? 'bg-red' : 'bg-blue'
        } py-3 px-4 text-white`}
      >
        <div className="flex">
          <div className="my-auto flex-auto">
            <p className="text-sm uppercase">{concept.type}</p>
            <h2 className="titlecase text-3xl font-semibold">{title}</h2>
            <p className="mr-5 ">{description}</p>
          </div>
          <div className="my-auto flex-none">
            <Link href={`/concepts/${concept.id}`}>
              <a className="border-2 border-white px-3 py-2 text-sm no-underline">
                Find out more →
              </a>
            </Link>
          </div>
        </div>
      </div>
    </>
  )
}

export default ConceptPanel
