// import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api'
import { useEffect, useRef } from 'react'
import tt from '@tomtom-international/web-sdk-maps'

const containerStyle = { width: '100%', height: '1000px' }
const center = { lng: -2.0, lat: 54.0 }

function Map() {
  const mapRef = useRef<HTMLDivElement | null>(null)
  const apiKey = import.meta.env.VITE_TOMTOM_API_KEY

  useEffect(() => {
    if (!mapRef.current) return

    const map = tt.map({
      key: apiKey,
      container: mapRef.current,
      center: center,
      zoom: 6,
    })

    new tt.Marker().setLngLat(center).addTo(map)

    return () => map.remove()
  }, [apiKey])

  return <div ref={mapRef} style={containerStyle}></div>
}

export default Map
