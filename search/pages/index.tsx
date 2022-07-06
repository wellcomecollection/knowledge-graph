import CardBlock from '../components/card-block'
import { CardProps } from '../components/card'
import Layout from '../components/layout'
import { NextPage } from 'next'

const Index: NextPage = () => {
  const exhibitionCards = [
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
  ]
  const storiesCards = [
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
    {
      imageURL:
        'https://images.prismic.io/wellcomecollection/3eb4b341-6471-4610-9f12-c97f5c7be0bc_SDP_20201005_0278-81.jpg?auto=compress%2Cformat&rect=0%2C0%2C2955%2C1662&w=2048&h=1152',
      imageAlt:
        'Photograph of a museum gallery space with display cases and exhibits. In the foreground is a woman wearing a face covering and a pair of yellow over the ear headphones. She is in the process of plugging the headphones into the socket of an audio exhibit. To the right of her is another woman also wearing a face covering who is looking up at a transparent model of human being. In the far distance is a man, also wearing a face covering who is exploring the exhibiton.',
      title: 'Being Human',
      description: 'Now on',
      URL: 'https://wellcomecollection.org/exhibitions/XNFfsxAAANwqbNWD',
      type: 'Permanent exhibition',
    },
  ]
  return (
    <Layout isHomePage>
      <CardBlock title="Exhibitions" cards={exhibitionCards as CardProps[]} />
      <CardBlock title="Stories" cards={storiesCards as CardProps[]} />
    </Layout>
  )
}

export default Index
