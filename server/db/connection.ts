// import knex from 'knex'
// import config from './knexfile.js'

// type Environment = 'development' | 'production' | 'test'
// const env = (process.env.NODE_ENV as Environment) || 'development'

// const connection = knex(config[env])

// export default connection

import knex from 'knex'
import config from './knexfile.js'

const env =
  (process.env.NODE_ENV as 'development' | 'production' | 'test') ||
  'development'

const db = knex(config[env])

// Quick test (optional)
db.raw('SELECT 1')
  .then(() => console.log('SQLite connected!'))
  .catch((err) => console.error('SQLite connection failed:', err))

export default db
