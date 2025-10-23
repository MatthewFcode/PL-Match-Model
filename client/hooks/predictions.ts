import { useQuery } from '@tanstack/react-query'

import { getPredictions } from '../apis/predictions.ts'

export function usePredictions() {
  const query = useQuery({ queryKey: ['predictions'], queryFn: getPredictions })
  return query
}
