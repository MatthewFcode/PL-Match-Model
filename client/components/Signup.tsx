import { IfAuthenticated, IfNotAuthenticated } from './Auth0.tsx'
import { useAuth0 } from '@auth0/auth0-react'
import { useState, useEffect } from 'react'

function Signup() {
  const [needsRegistration, setNeedsRegistration] = useState(false)
  const { logout, loginWithRedirect, isAuthenticated, getAccessTokenSilently } =
    useAuth0()

  useEffect =
    (() => {
      // async function getting yourself as a user
      if (!isAuthenticated) {
        return
      }
      const token = await getAccessTokenSilently()
      // make the api call
      // const data = await res.json()
      // if the data returns needs registration then set needs registration to true
    },
    [isAuthenticated])

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
