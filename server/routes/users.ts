import { Router } from 'express'
import * as db from '../db/users.ts'
import camelcaseKeys from 'camelcase-keys'
import multer from 'multer'
import cloudinary from '../cloudinary.js'
import { unlink } from 'node:fs/promises'
import { UserSnake } from '../../models/users.ts'
import checkJwt, { JwtRequest } from '../auth0'

const router = Router()
const upload = multer({ dest: 'tmp/' })

router.get('/', checkJwt, async (req: JwtRequest, res) => {
  console.log('REQ.AUTH:', req.auth) // log the token info
  res.json({ test: 'hello' })
  // try {
  //   const auth0Id = req.auth?.sub
  //   const yourself = await db.getUserByAuth0Id(auth0Id as string)
  //   if (!yourself) {
  //     return res.json({ needsRegistration: true })
  //   }

  //   const result = yourself ? camelcaseKeys(yourself, { deep: true }) : [] //switch from snake case to camel case in the route
  //   console.log(result)
  //   res.status(200).json(result)
  // } catch (err) {
  //   res.status(500).json('That was an internal server error')
  //   console.log(err)
  // }
})

//Post route that takes multi part form data in from the req.body and then takes out the file from the multer tmp path and sends it to coudinary and then that img url back into the convert and post it to the db
router.post(
  '/',
  checkJwt,
  upload.single('profile_photo'),
  async (req: JwtRequest, res) => {
    try {
      const auth0Id = req.auth?.sub
      let profile_photo_init = '' // variable to store the cloudinary url in

      if (req.file) {
        try {
          // Upload to Cloudinary
          const result = await cloudinary.uploader.upload(req.file.path, {
            folder: 'MatchModel',
            transformation: [{ width: 300, height: 300, crop: 'fill' }],
          })
          profile_photo_init = result.secure_url

          // Clean up temp file
          await unlink(req.file.path)
        } catch (uploadErr) {
          console.error('Cloudinary upload error:', uploadErr)
          // Clean up temp file even if upload fails
          try {
            await unlink(req.file.path)
          } catch (unlinkErr) {
            console.error('Failed to delete temp file:', unlinkErr)
          }
          throw new Error('Failed to upload image')
        }
      }

      const convert: UserSnake = {
        auth0Id: auth0Id as string,
        username: req.body.username,
        favourite_team: req.body.favouriteTeam,
        profile_photo: profile_photo_init,
      }

      const result = await db.postNewUser(convert)
      res.status(201).json(result)
    } catch (err) {
      res.status(400).json('Bad POST request')
      console.log(err)
    }
  },
)

router.delete('/', checkJwt, async (req: JwtRequest, res) => {
  try {
    const auth0Id = req.auth?.sub
    const result = await db.deleteUserByAuth0Id(auth0Id as string)
    console.log(result)
    res.json(result).status(204) // send the  2004 no content and then also the number of rows deleted as JSON
  } catch (err) {
    res.status(400).json('bad DELETE request')
    console.log(err)
  }
})

export default router
