import { IfAuthenticated, IfNotAuthenticated } from './Auth0.tsx'
import { useAuth0 } from '@auth0/auth0-react'
import { useState, useEffect } from 'react'
import { useGetUserByAuth0Id, usePostNewUser } from '../hooks/users.ts'

function Signup() {
  const [needsRegistration, setNeedsRegistration] = useState(false)
  const [placeholder, setPlaceholderState] = useState('')
  const [favouriteTeamPlaceholder, setFavouriteTeamPlaceholder] = useState('')
  //form state
  const [form, setForm] = useState({
    username: '',
    favouriteTeam: '',
    profilePhoto: null as File | null,
  })
  const { logout, loginWithRedirect, isAuthenticated, getAccessTokenSilently } =
    useAuth0()
  const addUser = usePostNewUser()

  // handling form changes
  const handleChange = (evt: React.ChangeEvent<HTMLInputElement>) => {
    evt.preventDefault()
    setForm({
      ...form,
      [evt.target.name]: evt.target.value,
    })
  }

  // handling the file change
  function handleFileChange(evt: React.ChangeEvent<HTMLInputElement>) {
    if (evt.target.files && evt.target.files[0]) {
      setForm({ ...form, profilePhoto: evt.target.files[0] })
    }
  }
  // submit handler
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    const token = await getAccessTokenSilently()
    evt.preventDefault()
    const formData = new FormData()
    formData.append('username', form.username)
    formData.append('favouriteTeam', form.favouriteTeam)
    if (form.profilePhoto) {
      formData.append('profilePhoto', form.profilePhoto)
    }
    await addUser.mutateAsync({ token, formData })
  }
  const mixedNames = [
    'Lara',
    'HexReaper',
    'Oscar',
    'TurboNova',
    'Ella',
    'ShadowViper',
    'Jasper',
    'GlitchWolf',
    'Ava',
    'NightCrawler',
    'Ethan',
    'AstralDagger',
    'Mia',
    'CyberSpectre',
    'Ruby',
    'VortexStrike',
    'Caleb',
    'NeonRogue',
    'Sophie',
    'IronFalcon',
  ]

  useEffect(() => {
    let index = 0
    const interval = setInterval(() => {
      setPlaceholderState(mixedNames[index])
      index = (index + 1) % mixedNames.length
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  const premierLeagueTeams = [
    'Arsenal',
    'Aston Villa',
    'AFC Bournemouth',
    'Brentford',
    'Brighton & Hove Albion',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Leeds United',
    'Liverpool',
    'Manchester City',
    'Manchester United',
    'Newcastle United',
    'Nottingham Forest',
    'Sunderland',
    'Tottenham Hotspur',
    'West Ham United',
    'Wolverhampton Wanderers',
  ]
  useEffect(() => {
    let index = 0
    const interval = setInterval(() => {
      setFavouriteTeamPlaceholder(premierLeagueTeams[index])
      index = (index + 1) % premierLeagueTeams.length
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  // useEffect making call to the backend and checking if route returns need registering and then setting the needs register state to true so the componentn shows the form
  useEffect(() => {
    if (!isAuthenticated) {
      return
    }
    async function checkRegistration() {
      try {
        const token = await getAccessTokenSilently()

        const result = await fetch('/api/v1/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await result.json()

        if (data.needsRegistration === true) {
          setNeedsRegistration(true)
        }
      } catch (err) {
        console.log('Profile check failed', err)
      }
    }
    checkRegistration()
  }, [isAuthenticated])

  const handleLogout = () => {
    logout({ logoutParams: { returnTo: window.location.origin } })
  }

  const handleLogin = () => {
    loginWithRedirect({
      authorizationParams: {
        redirectUri: `${window.location.origin}`,
      },
    })
  }

  return (
    <div>
      <IfNotAuthenticated>
        <h3>Welcome to the MatchModel home page ⚽ </h3>
        <h4>
          Create an account and choose your favourite football team or head
          straight to the prediction map 🗺️
        </h4>
        <button onClick={handleLogin}>Sign In</button>
      </IfNotAuthenticated>
      <IfAuthenticated>
        <button onClick={handleLogout}>Sign Out</button>
        {needsRegistration && (
          <div>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
              <label htmlFor="profilePhoto">Choose your profile photo</label>
              <input
                type="file"
                name="profilePhoto"
                id="profilePhoto"
                accept="image/*"
                onChange={handleFileChange}
              />
              <label htmlFor="username">
                Whats your user name going to be?
              </label>
              <input
                type="text"
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder={placeholder}
                required
              />
              <input
                type="text"
                name="favouriteTeam"
                onChange={handleChange}
                value={form.favouriteTeam}
                placeholder={favouriteTeamPlaceholder}
                required
              />
            </form>
          </div>
        )}
      </IfAuthenticated>
    </div>
  )
}

export default Signup
