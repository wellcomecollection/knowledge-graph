import { FC } from 'react'

type Props = {
  wikidata_id: string
  mesh_id: string
  lc_subjects_id: string
  lc_names_id: string
}
const IdTable: FC<Props> = ({
  wikidata_id,
  mesh_id,
  lc_subjects_id,
  lc_names_id,
}) => {
  const data = [
    {
      id: wikidata_id,
      label: 'Wikidata',
      url: `https://www.wikidata.org/wiki/${wikidata_id}`,
    },
    {
      id: mesh_id,
      label: 'MeSH',
      url: `https://meshb.nlm.nih.gov/record/ui?ui=${mesh_id}`,
    },
    {
      id: lc_subjects_id,
      label: 'LC Subjects',
      url: `https://id.loc.gov/authorities/subjects/${lc_subjects_id}.html`,
    },
    {
      id: lc_names_id,
      label: 'LC Names',
      url: `https://id.loc.gov/authorities/subjects/${lc_subjects_id}.html`,
    },
  ]

  return (
    <table className="w-full table-auto bg-paper-2">
      <thead className="border-b border-green">
        <tr className="text-left">
          <th className="px-2">Source</th>
          <th>ID</th>
        </tr>
      </thead>
      <tbody className="bg-paper-2">
        {data.map((item, index) => (
          <tr
            key={item.label}
            className={`${index % 2 == 0 ? 'bg-paper-3' : null}`}
          >
            <td className="px-2">{item.label}</td>
            <td>
              {item.id ? (
                <a href={item.url} className="no-underline">
                  {item.id}
                </a>
              ) : (
                '-'
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default IdTable
