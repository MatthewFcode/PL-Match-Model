import request from 'superagent'
import { UserCamel, AddUserFunction } from '.././../models/users.ts'

const rootURL = '/api/v1'

// NEWS FLASH: this function returns a promise | async automtically wraps the return value in a promise
export async function getUserByAuth0Id(token: string): Promise<UserCamel> {
  const result = await request
    .get(`${rootURL}/users`)
    .set('Authorization', `Bearer ${token}`)
  return result.body
}

// function for posting new user object takes the parameter of the object no?
export async function postNewUser({
  formData,
  token,
}: AddUserFunction): Promise<UserCamel> {
  const result = await request
    .post(`${rootURL}/users`)
    .set('Authorization', `Bearer ${token}`)
    .send(formData)
  return result.body
}

// function for sending HTTP delete request with the auth0Id
export async function deleteUser(token: string): Promise<number> {
  const result = await request
    .delete(`${rootURL}/users`)
    .set('Authorization', `Bearer ${token}`)
  return result.body
}
