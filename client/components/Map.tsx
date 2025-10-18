import { useState, useEffect } from 'react'
import { MapPin, TrendingUp, Calendar } from 'lucide-react'

function MatchPredictor() {
  const [map, setMap] = useState(null)
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [predictions, setPredictions] = useState(null)
  const [loading, setLoading] = useState(false)

  const teams = [
    { name: 'Arsenal', lat: 51.5549, lng: -0.1084, color: '#EF0107' },
    { name: 'Aston Villa', lat: 52.5086, lng: -1.8853, color: '#540D6E' },
    { name: 'Bournemouth', lat: 50.7352, lng: -1.8387, color: '#000000' },
    { name: 'Brighton', lat: 50.8619, lng: -0.0832, color: '#0057B8' },
    { name: 'Chelsea', lat: 51.4819, lng: -0.1909, color: '#034694' },
    { name: 'Everton', lat: 53.4387, lng: -2.6661, color: '#003DA5' },
    { name: 'Fulham', lat: 51.4755, lng: -0.2225, color: '#000000' },
    { name: 'Ipswich', lat: 52.0547, lng: 1.144, color: '#0053A0' },
    { name: 'Leicester', lat: 52.62, lng: -1.1422, color: '#0053A0' },
    { name: 'Liverpool', lat: 53.4308, lng: -2.9606, color: '#C8102E' },
    { name: 'Man City', lat: 53.483, lng: -2.2001, color: '#6CABDA' },
    { name: 'Man United', lat: 53.4629, lng: -2.2913, color: '#DA291C' },
    { name: 'Newcastle', lat: 54.9749, lng: -1.6214, color: '#241F20' },
    { name: 'Nottingham', lat: 52.9399, lng: -1.133, color: '#DD0000' },
    { name: 'Southampton', lat: 50.9061, lng: -1.3909, color: '#000000' },
    { name: 'Tottenham', lat: 51.6039, lng: -0.0661, color: '#132257' },
    { name: 'West Ham', lat: 51.5391, lng: 0.0161, color: '#7C2C3B' },
    { name: 'Wolverhampton', lat: 52.5098, lng: -2.1302, color: '#FDB913' },
  ]

  useEffect(() => {
    // Initialize map with Leaflet
    const script = document.createElement('script')
    script.src =
      'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js'
    script.async = true
    script.onload = () => {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href =
        'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css'
      document.head.appendChild(link)

      // Initialize map after Leaflet loads
      setTimeout(() => {
        const L = window.L
        const mapInstance = L.map('map').setView([53.5, -2], 6)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
          maxZoom: 19,
        }).addTo(mapInstance)

        // Add markers for each team
        teams.forEach((team) => {
          const marker = L.circleMarker([team.lat, team.lng], {
            radius: 10,
            fillColor: team.color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9,
          })
            .addTo(mapInstance)
            .bindPopup(`<strong>${team.name}</strong>`)

          marker.on('click', () => handleTeamClick(team))
        })

        setMap(mapInstance)
      }, 100)
    }
    document.head.appendChild(script)
  }, [])

  const handleTeamClick = async (team) => {
    setSelectedTeam(team)
    setLoading(true)
    setPredictions(null)

    // Simulate AI prediction - replace with your actual API call
    setTimeout(() => {
      const mockPredictions = [
        {
          opponent: 'Random PL Team',
          date: 'Next Match',
          winProbability: 0.62,
          drawProbability: 0.22,
          lossProbability: 0.16,
        },
        {
          opponent: 'Another Team',
          date: 'Match 2',
          winProbability: 0.55,
          drawProbability: 0.25,
          lossProbability: 0.2,
        },
        {
          opponent: 'Third Team',
          date: 'Match 3',
          winProbability: 0.48,
          drawProbability: 0.28,
          lossProbability: 0.24,
        },
        {
          opponent: 'Fourth Team',
          date: 'Match 4',
          winProbability: 0.71,
          drawProbability: 0.18,
          lossProbability: 0.11,
        },
        {
          opponent: 'Fifth Team',
          date: 'Match 5',
          winProbability: 0.59,
          drawProbability: 0.23,
          lossProbability: 0.18,
        },
      ]
      setPredictions(mockPredictions)
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="w-full h-screen flex flex-col bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="bg-slate-950 border-b border-slate-700 p-6">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <MapPin className="text-blue-400" size={32} />
          Premier League Stadium Predictor
        </h1>
        <p className="text-slate-400 mt-2">
          Click on a stadium to see AI-predicted match outcomes for the next 5
          matches
        </p>
      </div>

      <div className="flex flex-1 gap-6 p-6 overflow-hidden">
        <div className="flex-1 rounded-lg overflow-hidden shadow-2xl border border-slate-700">
          <div id="map" className="w-full h-full"></div>
        </div>

        <div className="w-96 bg-slate-800 rounded-lg shadow-2xl border border-slate-700 overflow-hidden flex flex-col">
          {selectedTeam ? (
            <>
              <div className="bg-gradient-to-r from-slate-700 to-slate-600 p-6 border-b border-slate-600">
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-full border-4 border-white"
                    style={{ backgroundColor: selectedTeam.color }}
                  ></div>
                  <h2 className="text-2xl font-bold text-white">
                    {selectedTeam.name}
                  </h2>
                </div>
              </div>

              {loading ? (
                <div className="flex-1 flex items-center justify-center">
                  <div className="text-center">
                    <div className="animate-spin w-12 h-12 border-4 border-slate-600 border-t-blue-400 rounded-full mx-auto mb-4"></div>
                    <p className="text-slate-300">Generating predictions...</p>
                  </div>
                </div>
              ) : predictions ? (
                <div className="flex-1 overflow-y-auto p-4 space-y-3">
                  {predictions.map((pred, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-700 rounded-lg p-4 border border-slate-600 hover:border-slate-500 transition"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <Calendar size={16} className="text-slate-400" />
                          <span className="text-sm font-semibold text-slate-300">
                            {pred.date}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 text-yellow-400">
                          <TrendingUp size={14} />
                          <span className="text-xs font-bold">
                            {Math.round(
                              Math.max(
                                pred.winProbability,
                                pred.drawProbability,
                                pred.lossProbability,
                              ) * 100,
                            )}
                            %
                          </span>
                        </div>
                      </div>
                      <p className="text-white font-semibold text-sm mb-3">
                        vs {pred.opponent}
                      </p>
                      <div className="space-y-2">
                        <div>
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs text-green-400 font-semibold">
                              Win
                            </span>
                            <span className="text-xs text-slate-200">
                              {Math.round(pred.winProbability * 100)}%
                            </span>
                          </div>
                          <div className="h-2 bg-slate-600 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-green-500"
                              style={{ width: `${pred.winProbability * 100}%` }}
                            ></div>
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs text-yellow-400 font-semibold">
                              Draw
                            </span>
                            <span className="text-xs text-slate-200">
                              {Math.round(pred.drawProbability * 100)}%
                            </span>
                          </div>
                          <div className="h-2 bg-slate-600 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-yellow-500"
                              style={{
                                width: `${pred.drawProbability * 100}%`,
                              }}
                            ></div>
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-xs text-red-400 font-semibold">
                              Loss
                            </span>
                            <span className="text-xs text-slate-200">
                              {Math.round(pred.lossProbability * 100)}%
                            </span>
                          </div>
                          <div className="h-2 bg-slate-600 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-red-500"
                              style={{
                                width: `${pred.lossProbability * 100}%`,
                              }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-6">
              <MapPin size={48} className="text-slate-500 mb-4" />
              <p className="text-slate-400">
                Click on a stadium marker on the map to see predictions
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MatchPredictor
