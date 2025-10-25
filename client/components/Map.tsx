// import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api'
import { useEffect, useRef } from 'react'
import tt from '@tomtom-international/web-sdk-maps'
import { useTeams } from '../hooks/teams.ts'
import '@tomtom-international/web-sdk-maps/dist/maps.css'

const containerStyle = { width: '100%', height: '1000px' }
const center = { lng: -2.0, lat: 54.0 }

function Map({ onTeamClick }: { onTeamClick: (name: string) => void }) {
  const mapRef = useRef<HTMLDivElement | null>(null)
  const apiKey = import.meta.env.VITE_TOMTOM_API_KEY

  const {
    data: teams,
    isLoading: isTeamsLoading,
    isError: isTeamsError,
  } = useTeams()
  useEffect(() => {
    if (!mapRef.current || !teams) return

    const map = tt.map({
      key: apiKey,
      container: mapRef.current,
      center,
      zoom: 6,
    })

    const createdMarkers: tt.Marker[] = []

    teams.forEach((team) => {
      if (!team.stadium_lat || !team.stadium_lng) return

      const el = document.createElement('div')
      el.style.width = '40px'
      el.style.height = '40px'

      const img = document.createElement('img')
      img.src = team.team_logo
      img.style.width = '100%'
      img.style.height = '100%'
      img.style.borderRadius = '50%'
      img.style.cursor = 'pointer'
      img.style.display = 'block'
      img.style.border = '2px solid white'

      el.appendChild(img)

      const marker = new tt.Marker({ element: el, anchor: 'center' })
        .setLngLat([team.stadium_lng, team.stadium_lat])
        .addTo(map)

      el.addEventListener('click', () => {
        onTeamClick(team.team_name)
      })

      createdMarkers.push(marker)
    })

    return () => {
      createdMarkers.forEach((marker) => marker.remove())
      map.remove()
    }
  }, [teams, apiKey])

  if (isTeamsLoading) {
    return <div>...Loading</div>
  }

  if (isTeamsError) {
    return <div>Error loading teams</div>
  }

  return <div ref={mapRef} style={containerStyle}></div>
}

export default Map
