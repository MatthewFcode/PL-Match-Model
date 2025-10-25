import connection from './connection'
import { Team } from '../../models/teams.ts'

const db = connection

export async function getTeams(): Promise<Team[] | undefined> {
  try {
    const teams = await db('teams').select()
    console.log(teams)
    return teams
  } catch (err) {
    console.log(err)
  }
}
