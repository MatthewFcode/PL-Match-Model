import connection from './connection.ts'
import { UserSnake } from '../../models/users.ts'

const db = connection

// function for getting the user by the current auth0Id that is logged in
export async function getUserByAuth0Id(
  auth0Id: string,
): Promise<UserSnake | undefined> {
  try {
    const result = await db('users')
      .select()
      .where('users.auth0Id', auth0Id)
      .first()
    console.log(result)
    return result
  } catch (err) {
    console.log(err)
  }
}

//function for posting a whole user object to the data base
export async function postNewUser(
  newUser: UserSnake,
): Promise<UserSnake | undefined> {
  try {
    const result = await db('users').insert(newUser).returning('*').first()
    console.log(result)
    return result
  } catch (err) {
    console.log(err)
  }
}

// function deleting an account by the auth0Id
export async function deleteUserByAuth0Id(
  auth0Id: string,
): Promise<number | undefined> {
  try {
    const result = await db('users').where('users.auth0Id', auth0Id).delete() // REFRESHER ALERT .delete() in Knex returns a number specifaclly (the number of rows that were deleted) so this function should always return one as it deletes one user row from the table
    return result
  } catch (err) {
    console.log(err)
  }
}
