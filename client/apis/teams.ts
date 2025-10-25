import request from 'superagent'
import { Team } from '../../models/teams.ts'

const BASE_URL = '/api/v1/teams'

export async function getAllTeams(): Promise<Team[] | undefined> {
  try {
    const result = await request.get(`${BASE_URL}`)
    console.log(result.body)
    return result.body as Team[]
  } catch (err) {
    console.log(err)
  }
}

export async function getPredicitonsByName(
  name: string,
): Promise<Team[] | undefined> {
  try {
    const result = await request.get(`${BASE_URL}/predictions/${name}`)
    console.log(result)
    return result.body
  } catch (err) {
    console.log(err)
  }
}
