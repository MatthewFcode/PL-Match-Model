import { useTeamPredictions } from '../hooks/predictions.ts'
import { useTeams } from '../hooks/teams.ts'

interface PredictionOverlayProps {
  teamName: string
  onClose: () => void
}

const PredictionOverlay = ({ teamName, onClose }: PredictionOverlayProps) => {
  const { data: predictions, isLoading, isError } = useTeamPredictions(teamName)
  const { data: teams } = useTeams()

  // Helper function to get team logo by team name
  const getTeamLogo = (teamName: string) => {
    const team = teams?.find(
      (t) => t.team_name.toLowerCase() === teamName.toLowerCase(),
    )
    return team?.team_logo || ''
  }

  if (isLoading) {
    return (
      <div className="loading-overlay">
        <div className="loading-spinner"></div>
        <div className="loading-text">Loading predictions...</div>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="error-overlay">
        <div className="error-content">
          <p>Error loading predictions</p>
          <button className="close-button" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="prediction-overlay">
      <img
        src="/images/back.png"
        alt="Back"
        className="overlay-back-button"
        onClick={onClose}
      />
      <div className="prediction-content">
        <h2>{teamName} Upcoming Match Predictions ⚽</h2>
        {predictions?.map((match) => {
          const homeTeamLogo = getTeamLogo(match.homeTeam)
          const awayTeamLogo = getTeamLogo(match.awayTeam)
          const isHomeWinner =
            match.winningTeam.toLowerCase() === match.homeTeam.toLowerCase()
          const isAwayWinner =
            match.winningTeam.toLowerCase() === match.awayTeam.toLowerCase()

          return (
            <div key={match.date} className="match-card">
              <p className="match-date">{match.date}</p>

              <div className="match-teams-container">
                <div
                  className={`team-logo-section ${isHomeWinner ? 'winner-indicator' : ''}`}
                >
                  <img
                    src={homeTeamLogo}
                    alt={match.homeTeam}
                    className="team-logo"
                  />
                  <span className="team-name">{match.homeTeam}</span>
                </div>

                <span className="vs-divider">VS</span>

                <div
                  className={`team-logo-section ${isAwayWinner ? 'winner-indicator' : ''}`}
                >
                  <img
                    src={awayTeamLogo}
                    alt={match.awayTeam}
                    className="team-logo"
                  />
                  <span className="team-name">{match.awayTeam}</span>
                </div>
              </div>

              <div className="match-prediction">
                🏆 Predicted Winner: {match.winningTeam}
              </div>

              <p className="match-explanation">{match.explanation}</p>
            </div>
          )
        })}
        {/* <button className="close-button" onClick={onClose}>
          Close
        </button> */}
      </div>
    </div>
  )
}

export default PredictionOverlay
