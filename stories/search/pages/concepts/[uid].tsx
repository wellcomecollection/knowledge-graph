import { GetServerSideProps, NextPage } from 'next'

import { Concept as ConceptType } from '../../types/elasticsearch'
import Layout from '../../components/Layout'
import { getClient } from '../../services/elasticsearch'

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { uid: id } = params as { uid: string }
  const client = await getClient()
  const response = await client.get({ index: 'concepts', id })
  return { props: response.body._source }
}

const Concept: NextPage<ConceptType> = (props) => {
  const { id, name, variants, description, stories } = props
  return (
    <Layout title={name} description={description}>
      <h1 className="capitalize">{name}</h1>
      <p>{description}</p>
      <div className="pt-4">
        <h2 className="text-lg">Variant names</h2>
        <ul>
          {variants.split(',').map((variant) => (
            <li
              className="inline-block bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700 capitalize mr-2"
              key={variant}
            >
              {variant}
            </li>
          ))}
        </ul>
      </div>
      <div className="pt-4">
        <h2 className="text-lg">Stories</h2>
        <ul>
          {stories.split(',').map((story) => (
            <li
              className="inline-block bg-gray-200 rounded-lg px-2 py-1 text-xs text-gray-700 capitalize mr-2"
              key={story}
            >
              {story}
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  )
}

export default Concept
