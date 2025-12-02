export interface UserSnake {
  auth0Id: string
  username: string
  favourite_team: string
  profile_photo: string
}

export interface UserCamel {
  auth0Id: string
  username: string
  favouriteTeam: string
  profilePhoto: string
}

export interface AddUserFunction {
  formData: FormData
  token: string
}
