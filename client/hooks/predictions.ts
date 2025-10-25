import { useQuery } from '@tanstack/react-query'

import { getPredictions, getPredicitonsByName } from '../apis/predictions.ts'

export function usePredictions() {
  const query = useQuery({ queryKey: ['predictions'], queryFn: getPredictions })
  return query
}

export function useTeamPredictions(name: string) {
  const query = useQuery({
    queryKey: ['team-predictions'],
    queryFn: () => getPredicitonsByName(name),
  })

  return query
}
