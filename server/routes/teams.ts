import { Router } from 'express'
import { Team } from '../../models/teams.ts'
import { getTeams } from '../db/teams.ts'

const router = Router()

router.get('/', async (req, res) => {
  try {
    const result = (await getTeams()) as Team[]
    console.log(result)
    res.status(200).json(result)
  } catch (err) {
    console.log(err)
    res.status(500).json('something went wrong')
  }
})

export default router
