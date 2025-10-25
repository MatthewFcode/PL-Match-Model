import express from 'express'
import * as Path from 'node:path'

import predictionRoutes from './routes/predictions.ts'
import teamRoutes from './routes/teams.ts'

const server = express()

server.use(express.json())

server.use('/api/v1/predictions', predictionRoutes)
server.use('/api/v1/teams', teamRoutes)

if (process.env.NODE_ENV === 'production') {
  server.use(express.static(Path.resolve('public')))
  server.use('/assets', express.static(Path.resolve('./dist/assets')))
  server.get('*', (req, res) => {
    res.sendFile(Path.resolve('./dist/index.html'))
  })
}

export default server
