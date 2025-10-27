import connection from './connection.ts'
import { PredictionSnake } from '../../models/predictions.ts'

const db = connection

export async function getTeamByName(
  name: string,
): Promise<PredictionSnake[] | undefined> {
  try {
    const result = await db('predictions')
      .select()
      .where('predictions.home_team', name)
      .orWhere('predictions.away_team', name)
      .limit(5)
    console.log(result)
    return result
  } catch (err) {
    console.log(err, 'could not select the results from the database')
  }
}
