import { GetServerSideProps, NextPage } from 'next'

import { Concept as ConceptType } from '../../types/elasticsearch'
import Layout from '../../components/Layout'
import { getClient } from '../../services/elasticsearch'

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { id } = params as { id: string }
  const client = await getClient()
  const response = await client.get({
    index: process.env.ELASTIC_CONCEPTS_INDEX as string,
    id,
  })
  return { props: response.body._source }
}

const Concept: NextPage<ConceptType> = (props) => {
  const description = props.mesh_description || props.wikidata_description
  const title =
    props.wikidata_preferred_name ||
    props.mesh_preferred_name ||
    props.lcsh_preferred_name ||
    props.name

  return (
    <Layout title={title} description={description}>
      <h1>{title}</h1>
      <p>{description}</p>
      <div className="mt-4 pl-1 bg-gray-200 rounded text-sm py-2 space-y-1">
        <table className="table-auto">
          <tbody>
            <tr>
              <td className="pr-4 font-semibold">Wikidata ID</td>
              <td>
                <a
                  href={`https://www.wikidata.org/wiki/${props.wikidata_id}`}
                  className="no-underline"
                >
                  {props.wikidata_id}
                </a>
              </td>
            </tr>
            <tr>
              <td className="font-semibold">MeSH ID</td>
              <td>
                <a
                  href={`https://meshb.nlm.nih.gov/record/ui?ui=${props.mesh_id}`}
                  className="no-underline"
                >
                  {props.mesh_id}
                </a>
              </td>
            </tr>
            <tr>
              <td className="font-semibold">LCSH ID</td>
              <td>
                <a
                  href={`https://id.loc.gov/authorities/names/${props.lcsh_id}.html`}
                  className="no-underline"
                >
                  {props.lcsh_id}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      {props.variants ? (
        <div className="pt-4">
          <h2 className="text-lg">Also known as</h2>
          <ul>
            {props.variants.split('<BREAK>').map((variant) => (
              <li
                className="inline-block bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700 capitalize mr-2"
                key={variant}
              >
                {variant}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      <div className="pt-4">
        <h2 className="text-lg">Stories</h2>
        <ul className="leading-7">
          {props.stories.split('<BREAK>').map((story, index) => (
            <li key={story} className="inline-block">
              <a
                href={`https://wellcomecollection.org/articles/${
                  props.story_ids.split('<BREAK>')[index]
                }`}
                className="no-underline bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700 capitalize mr-2"
              >
                {story}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  )
}

export default Concept
