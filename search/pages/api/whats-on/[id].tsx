import { NextApiRequest, NextApiResponse } from 'next'
import { getClient, getWhatsOn } from '../../../services'

export default async function searchEndpoint(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    try {
      const { id } = req.query
      const client = getClient()
      const whatsOn = await getWhatsOn(client, id as string)
      res.status(200).json({
        ...whatsOn,
      })
    } catch {
      res.status(500).json({ error: 'Unable to query' })
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' })
  }
}
