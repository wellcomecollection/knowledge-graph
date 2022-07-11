import { NextApiRequest, NextApiResponse } from 'next'
import { getClient, getPerson } from '../../../services/elasticsearch'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const { id } = req.query
      const client = getClient()
      const person = await getPerson(client, id)
      res.status(200).json({
        ...person,
      })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
