import { useQuery } from '@tanstack/react-query'

import { getPredictions, getPredicitonsByName } from '../apis/predictions.ts'

export function usePredictions() {
  const query = useQuery({ queryKey: ['predictions'], queryFn: getPredictions })
  return query
}

export function useTeamPredictions(name: string) {
  const query = useQuery({
    queryKey: ['team-predictions', name], // need to include name in the query key because when the clicking on another team react query will look in the cache and find that data under the same query kay and load the cached data then replace it -- adding the name give each team a unique querykey so the other teams arent loaded through that cache
    queryFn: () => getPredicitonsByName(name),
    enabled: !!name, // stops the query from running if name isnt defined upon the component mount
  })

  return query
}
