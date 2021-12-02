import { GetServerSideProps, NextPage } from 'next'

import { Concept as ConceptType } from '../../types/elasticsearch'
import Layout from '../../components/Layout'
import { getClient } from '../../services/elasticsearch'

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  const { id } = params as { id: string }
  const client = await getClient()
  const response = await client.get({ index: 'concepts', id })
  return { props: response.body._source }
}

const Concept: NextPage<ConceptType> = (props) => {
  const { name, variants, description, stories, story_ids } = props

  return (
    <Layout title={name} description={description}>
      <h1 className="capitalize">{name}</h1>
      <p>{description}</p>
      {variants ? (
        <div className="pt-4">
          <h2 className="text-lg">Also known as</h2>
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
      ) : null}
      <div className="pt-4">
        <h2 className="text-lg">Stories</h2>
        <ul className="leading-7">
          {stories.split(',').map((story, index) => (
            <li key={story} className="inline-block">
              <a
                href={`https://wellcomecollection.org/articles/${
                  story_ids.split(',')[index]
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
