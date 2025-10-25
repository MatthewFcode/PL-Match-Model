import { useQuery } from '@tanstack/react-query'
import { getAllTeams } from '../apis/teams.ts'

export function useTeams() {
  const query = useQuery({ queryKey: ['teams'], queryFn: getAllTeams })
  return query
}
