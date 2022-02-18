import { FC } from 'react'

type Props = {
  wikidata_id: string
  mesh_id: string
  lcsh_id: string
}
const IdTable: FC<Props> = ({ wikidata_id, mesh_id, lcsh_id }) => {
  return (
    <div className="mt-4 space-y-1 rounded bg-gray-200 py-2 pl-1 text-sm">
      <table className="table-auto">
        <tbody>
          <tr>
            <td className="pr-4 font-semibold">Wikidata ID</td>
            <td>
              <a
                href={`https://www.wikidata.org/wiki/${wikidata_id}`}
                className="no-underline"
              >
                {wikidata_id}
              </a>
            </td>
          </tr>
          <tr>
            <td className="font-semibold">MeSH ID</td>
            <td>
              <a
                href={`https://meshb.nlm.nih.gov/record/ui?ui=${mesh_id}`}
                className="no-underline"
              >
                {mesh_id}
              </a>
            </td>
          </tr>
          <tr>
            <td className="font-semibold">LCSH ID</td>
            <td>
              <a
                href={`https://id.loc.gov/authorities/subjects/${lcsh_id}.html`}
                className="no-underline"
              >
                {lcsh_id}
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default IdTable
