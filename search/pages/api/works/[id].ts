import { NextApiRequest, NextApiResponse } from 'next'
import { getClient, getWork } from '../../../services'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const client = getClient()
      const work = await getWork(client, req.query.id as string)
      res.status(200).json(work)
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
