import { GetServerSideProps, NextPage } from 'next'

type Props = {}

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  return {
    props: {},
  }
}

const Concept: NextPage<Props> = (props) => {
  return <div className="" />
}

export default Concept
