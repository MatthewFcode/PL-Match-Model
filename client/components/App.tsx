import Map from './Map.tsx'
import { useState } from 'react'
import PredictionOverlay from './PredictionOverlay.tsx'

function App() {
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null)
  return (
    <>
      <div className="app">
        <Map onTeamClick={(name) => setSelectedTeam(name)} />
      </div>

      {selectedTeam && (
        <PredictionOverlay
          teamName={selectedTeam}
          onClose={() => setSelectedTeam(null)}
        />
      )}
    </>
  )
}

export default App
