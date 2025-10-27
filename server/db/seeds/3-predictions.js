import superagent from 'superagent'

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */

const PREDICTIONS_URL = 'http://localhost:5000/predictions'
async function getAllPredictions() {
  const result = await superagent.get(`${PREDICTIONS_URL}`)
  return result.body
}
export async function seed(knex) {
  try {
    const predictions = await getAllPredictions()

    const formattedPredictions = predictions.map((p) => ({
      away_team: p.away_team,
      date: p.date,
      explanation: p.explanation,
      home_team: p.home_team,
      winning_team: p.winning_team,
    }))
    // wipe the old prediction when running the seed
    await knex('predictions').del()
    // insert the newly fetched ones
    await knex('predictions').insert(formattedPredictions)
  } catch (err) {
    console.log(err)
    console.log('There was an error seeding predictions')
  }
}
