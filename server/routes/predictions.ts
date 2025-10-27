import { Router } from 'express'
import superagent from 'superagent'
const router = Router()
import { PredictionSnake, PredictionCamel } from '../../models/predictions.ts'
import * as db from '../db/predictions.ts'

const BASE_URL = 'http://localhost:5000'

router.get('/', async (req, res) => {
  try {
    const { body } = await superagent.get(`${BASE_URL}/predictions`) // gets the body object that from the response object that returns the status e.t.c

    const predictions: PredictionCamel[] = body.map(
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

router.get('/:name', async (req, res) => {
  try {
    const { name } = req.params

    const snakeCasePredictions = await db.getTeamByName(name)

    const predictions: PredictionCamel[] = (snakeCasePredictions || []).map(
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
  } catch (err) {
    console.log(err)
    res.status(500).json('Something went wrong')
  }
})

// OLD PREDICTION ROUTE FOR GETTING THE PREDICTIONS FROM THE NAME OF THE TEAM AND SENDING IT TO THE BACK END API
// router.get('/:name', async (req, res) => {
//   try {
//     const { name } = req.params
//     const { body } = await superagent.get(`${BASE_URL}/predictions/${name}`)

//     const predictions: PredictionCamel = body.map(
//       ({
//         away_team,
//         date,
//         explanation,
//         home_team,
//         winning_team,
//       }: PredictionSnake) => ({
//         awayTeam: away_team,
//         date,
//         explanation,
//         homeTeam: home_team,
//         winningTeam: winning_team,
//       }),
//     )

//     res.status(200).json(predictions)
//   } catch (err) {
//     console.log(err)
//     res.status(500).json('Something went wrong')
//   }
// })

export default router
