import { GetServerSideProps, NextPage } from 'next'
import { getClient, getWork } from '../../services'

import Head from 'next/head'
import Layout from '../../components/layout'
import { Work } from '../../types/work'

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
      source: string
    }[]
  }[]
}

export type wecoApiWork = {
  subjects: {
    id: string
    label: string
    type: string
    concepts: {
      id: string
      label: string
      type: string
    }[]
  }[]
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
  console.log(originalWorkSubjects)
  console.log(work.subjects)
  const subjectComparisonTable = originalWorkSubjects.map((originalSubject) => {
    return {
      original: originalSubject,
      enriched: work.subjects
        .filter(
          (enrichedSubject) =>
            enrichedSubject.parent_label === originalSubject.label
        )
        .map((enrichedSubject) => {
          return {
            label: enrichedSubject.label,
            id: enrichedSubject.id,
            type: enrichedSubject.type,
            source: enrichedSubject ? enrichedSubject.source : '',
          }
        }),
    }
  })
  return {
    props: {
      work,
      subjectComparisonTable,
    },
  }
}

const WorkPage: NextPage<Props> = ({ work, subjectComparisonTable }) => {
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
          </div>
        </div>
        <div className="mx-auto space-y-8 px-5 lg:w-3/4">
          <h2 className="font-sans font-light">About this work</h2>
          <a href={`https://wellcomecollection.org/works/${work.id}`}>
            Original work page
          </a>
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
              {work.subjects.reverse().map((subject) => (
                <li key={subject.id} className="pb-6">
                  <a
                    className="w-100 rounded-full border border-gray-400 py-2 px-3 text-sm capitalize no-underline"
                    href={`/${
                      subject.type == 'Subject' ? 'subjects' : 'people'
                    }/${subject.id}`}
                  >
                    {subject.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div>
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
                      <td className="pl-1 pr-3">
                        {subject.enriched.map((subject) => (
                          <li key={subject.id}>
                            <a
                              href={`/${
                                subject.type == 'Subject'
                                  ? 'subjects'
                                  : 'people'
                              }/${subject.id}`}
                            >
                              <span className="capitalize">
                                {subject.label}{' '}
                              </span>
                              (label from {subject.source})
                            </a>
                            <br />
                          </li>
                        ))}
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
