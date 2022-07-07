import { GetServerSideProps, NextPage } from 'next'

import Head from 'next/head'
import Layout from '../../components/layout'
import { Work } from '../../types/work'
import { getClient } from '../../services/elasticsearch'
import { getWork } from '../../services/elasticsearch/work'
import { useState } from 'react'

type Props = {
  work: Work
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const workId = query.id as string
  const client = getClient()
  const work = await getWork(client, workId)
  return { props: { work } }
}

const WorkPageTabs = ['Catalogue details', 'View', 'Related']
type WorkPageTabType = typeof WorkPageTabs[number]

const WorkPage: NextPage<Props> = ({ work }) => {
  const [selectedTab, setSelectedTab] = useState(
    'Catalogue details' as WorkPageTabType
  )
  return (
    <div className="">
      <Head>
        <title>{work.title}</title>
      </Head>
      <Layout>
        <div className="bg-paper-1">
          <div className="mx-auto  px-5 pt-8 lg:w-3/4">
            <div className="flex flex-col items-start space-y-1">
              <p className="my-1 bg-paper-3 py-1 px-2 text-xs font-bold capitalize ">
                {work.type}
              </p>
            </div>
            <h1 className="font-sans">{work.title}</h1>
            <p className="py-2 text-sm capitalize">
              2007 | {work.contributors.map((c) => c.name).join(', ')}
            </p>

            <ul className="flex divide-gray-400 border-b pt-4">
              {WorkPageTabs.map((tab) => {
                return (
                  <li key={tab}>
                    <button
                      className={`inline h-full border-yellow px-4 py-3 no-underline ${
                        selectedTab == tab ? 'border-b-4' : ''
                      }`}
                      onClick={() => setSelectedTab(tab as WorkPageTabType)}
                    >
                      {tab}
                    </button>
                  </li>
                )
              })}
            </ul>
          </div>
        </div>
        <div className="mx-auto space-y-8 px-5 lg:w-3/4">
          <h2 className="font-sans font-light">About this work</h2>

          <div>
            <p className="font-bold">Description</p>
            <p>{work.description}</p>
          </div>
          <div>
            <p className="font-bold">Contributors</p>
            <ul className="flex capitalize">
              {work.contributors.map((contributor) => (
                <li key={contributor.id}>
                  <a className="" href={`/people/${contributor.id}`}>
                    {contributor.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="font-sans font-light">Related subjects</h2>
            <ul className="flex flex-wrap gap-x-2 pt-4">
              {work.concepts.map((concept) => (
                <li key={concept.id} className="pb-6">
                  <a
                    className="w-100 rounded-full border border-gray-400 py-2 px-3 text-sm capitalize no-underline"
                    href={`/subjects/${concept.id}`}
                  >
                    {concept.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Layout>
    </div>
  )
}

export default WorkPage
