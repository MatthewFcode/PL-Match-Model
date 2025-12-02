import { IfAuthenticated, IfNotAuthenticated } from './Auth0.tsx'
import { useAuth0 } from '@auth0/auth0-react'
import { useState, useEffect } from 'react'
import { useGetUserByAuth0Id, usePostNewuser } from '../hooks/users.ts'

function Signup() {
  const [needsRegistration, setNeedsRegistration] = useState(false)

  const { logout, loginWithRedirect, isAuthenticated, getAccessTokenSilently } =
    useAuth0()
  // useEffect making call to the backend and checking if route returns need registering and then setting the needs register state to true so the componentn shows the form
  useEffect(() => {
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
        {needsRegistration && <div>Sign Up you numpty</div>}
      </IfAuthenticated>
    </div>
  )
}

export default Signup
