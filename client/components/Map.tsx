import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api'

const containerStyle = { width: '100%', height: '1000px' }
const center = { lat: -36.848461, lng: 174.763336 }

function Map() {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  })

  if (!isLoaded) return <div>Loading Map...</div>
  console.log(import.meta.env.VITE_GOOGLE_MAPS_API_KEY)

  return (
    <div className="map-container">
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={12}>
        {/* Example marker */}
        <Marker position={center} />
      </GoogleMap>
    </div>
  )
}

export default Map
