import { Router } from 'express'
import superagent from 'superagent'
const router = Router()
import { PredictionSnake, PredictionCamel } from '../../models/predictions.ts'

const BASE_URL = 'http://localhost:5000'

router.get('/', async (req, res) => {
  try {
    const { body } = await superagent.get(`${BASE_URL}/predictions`) // gets the body object that from the response object that returns the status e.t.c

    const predictions: PredictionCamel = body.map(
      ({
        away_team,
        date,
        explanation,
        home_team,
        winning_team,
      }: PredictionSnake) => ({
        awayTeam: away_team,
        date,
        explanation,
        homeTeam: home_team,
        winningTeam: winning_team,
      }),
    )
    res.status(200).json(predictions)
    console.log(predictions)
  } catch (error) {
    console.log(error)
    res.status(500).json('Something went wrong')
  }
})

export default router
