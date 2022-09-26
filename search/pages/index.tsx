import { GetServerSideProps, NextPage } from 'next'
import { Story, StoryHit } from '../types/story'
import { WhatsOn, WhatsOnHit } from '../types/whats-on'
import { getClient, parseStory } from '../services'

import CardBlock from '../components/card-block'
import { CardProps } from '../components/card'
import Layout from '../components/layout'
import { parseWhatsOn } from '../services'

type Props = {
  whatsOns: WhatsOn[]
  stories: Story[]
}

export const getServerSideProps: GetServerSideProps = async () => {
  const client = getClient()
  const whatsOns = await client
    .search({
      index: process.env.ELASTIC_WHATS_ON_INDEX,
      body: {
        query: {
          match_all: {},
        },
        size: 3,
      },
    })
    .then((res) => {
      return res.body.hits.hits.map((hit: WhatsOnHit) => parseWhatsOn(hit))
    })

  const stories = await client
    .search({
      index: process.env.ELASTIC_STORIES_INDEX,
      body: {
        query: {
          match_all: {},
        },
        size: 3,
      },
    })
    .then((res) => {
      return res.body.hits.hits.map((hit: StoryHit) => parseStory(hit))
    })

  return {
    props: { whatsOns, stories },
  }
}

const Index: NextPage<Props> = ({ whatsOns, stories }) => {
  const whatsOnCards: CardProps[] = whatsOns.map((whatsOn) => ({
    title: whatsOn.title,
    description: '',
    imageURL: whatsOn.image_url,
    imageAlt: whatsOn.image_alt,
    URL: `https://wellcomecollection.org/exhibition/${whatsOn.id}`,
    type: whatsOn.format,
  }))

  const storyCards: CardProps[] = stories.map((story) => ({
    title: story.title,
    description: '',
    imageURL: '',
    imageAlt: '',
    URL: `https://wellcomecollection.org/articles/${story.id}`,
    type: 'story',
  }))
  return (
    <Layout isHomePage>
      <CardBlock title="What's on" cards={whatsOnCards as CardProps[]} />
      <CardBlock title="Stories" cards={storyCards as CardProps[]} />
    </Layout>
  )
}

export default Index
