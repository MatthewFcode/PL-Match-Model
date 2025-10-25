import request from 'superagent'
import { PredictionCamel } from '../../models/predictions'

const BASE_URL = '/api/v1/predictions'

export async function getPredictions(): Promise<PredictionCamel[] | undefined> {
  try {
    const result = await request.get(`${BASE_URL}`)
    console.log(result.body)
    return result.body as PredictionCamel[]
  } catch (err) {
    console.log(err)
  }
}

export async function getPredicitonsByName(
  name: string,
): Promise<PredictionCamel[] | undefined> {
  try {
    const result = await request.get(`${BASE_URL}/${name}`)
    console.log(result)
    return result.body
  } catch (err) {
    console.log(err)
  }
}
