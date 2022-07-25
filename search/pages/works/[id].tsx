import { GetServerSideProps, NextPage } from 'next'

import Head from 'next/head'
import Layout from '../../components/layout'
import { Work } from '../../types/work'
import { getClient } from '../../services/elasticsearch'
import { getWork } from '../../services/elasticsearch/work'
import { useState } from 'react'

type Props = {
  work: Work
  subjectComparisonTable: {
    original: {
      label: string
      id: string
    }
    enriched: {
      label: string
      type: string
      id: string
    }
  }[]
}

export type wecoApiWork = {
  subjects?: any[]
  title: string
  id: string
  type: string
}

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const workId = query.id as string
  const client = getClient()
  const work = await getWork(client, workId)
  const originalWork: wecoApiWork = await fetch(
    `https://api.wellcomecollection.org/catalogue/v2/works/${workId}?include=subjects`
  ).then((res) => res.json())

  const originalWorkSubjects = originalWork.subjects
    ? originalWork.subjects
    : []
  const subjectComparisonTable = originalWorkSubjects.map((originalSubject) => {
    const enrichedSubject = work.concepts.find(
      (enrichedSubject) =>
        enrichedSubject.originalLabel === originalSubject.label
    )
    return {
      original: {
        label: originalSubject.label ? originalSubject.label : '',
        id: originalSubject.id ? originalSubject.id : '',
      },
      enriched: {
        label: enrichedSubject ? enrichedSubject.label : '',
        id: enrichedSubject ? enrichedSubject.id : '',
        type: enrichedSubject ? enrichedSubject.type : '',
      },
    }
  })

  return {
    props: {
      work,
      subjectComparisonTable,
    },
  }
}

const WorkPageTabs = ['Catalogue details', 'View', 'Related']
type WorkPageTabType = typeof WorkPageTabs[number]

const WorkPage: NextPage<Props> = ({ work, subjectComparisonTable }) => {
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
              {work.published}
              {work.contributors.length > 0 &&
                work.published.length > 0 &&
                ' | '}
              {work.contributors.map((c) => c.label).join(', ')}
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
          {work.description && (
            <div>
              <p className="font-bold">Description</p>
              <p>{work.description}</p>
            </div>
          )}
          {work.contributors.length > 0 && (
            <div>
              <p className="font-bold">Contributors</p>
              <ul className="capitalize">
                {work.contributors.map((contributor) => (
                  <li key={contributor.id}>
                    <a href={`/people/${contributor.id}`}>
                      {contributor.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
          <div>
            <p className="font-bold">Subjects</p>
            <ul className="flex flex-wrap gap-x-2 pt-4">
              {work.concepts.map((concept) => (
                <li key={concept.id} className="pb-6">
                  <a
                    className="w-100 rounded-full border border-gray-400 py-2 px-3 text-sm capitalize no-underline"
                    href={`/${
                      concept.type == 'subject' ? 'subjects' : 'people'
                    }/${concept.id}`}
                  >
                    {concept.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="font-bold">
              Subjects compared to the{' '}
              <a href={`https://wellcomecollection.org/works/${work.id}`}>
                original work page
              </a>
            </p>
            <div className="pt-4">
              <table className="table-fixed ">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pl-1 pr-3">Original</th>
                    <th className="pl-1 pr-3">Enriched</th>
                  </tr>
                </thead>
                <tbody>
                  {subjectComparisonTable.map((subject, i) => (
                    <tr
                      key={subject.original.id ? subject.original.id : i}
                      className={i % 2 == 0 ? 'bg-gray-100' : ''}
                    >
                      <td className="pl-1 pr-3">{subject.original.label}</td>
                      <td className="pl-1 pr-3 capitalize">
                        <a
                          href={`/${
                            subject.enriched.type == 'subject'
                              ? 'subjects'
                              : 'people'
                          }/${subject.enriched.id}`}
                        >
                          {subject.enriched.label}
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </Layout>
    </div>
  )
}

export default WorkPage
