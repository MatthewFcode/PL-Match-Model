import { useAuth0 } from '@auth0/auth0-react'
import {
  useQuery,
  useMutation,
  MutationFunction,
  useQueryClient,
} from '@tanstack/react-query'
import * as API from '../apis/users.ts'

export function useGetUserByAuth0Id() {
  const { user, getAccessTokenSilently } = useAuth0()
  const result = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const token = await getAccessTokenSilently()
      API.getUserByAuth0Id(token)
    },
    enabled: !!user,
  })
  return result
}

export function useUserMutation<TData = unknown, TVariables = unknown>(
  mutationFn: MutationFunction<TData, TVariables>,
) {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user'] })
    },
  })

  return mutation
}

export function usePostNewUser() {
  // wrapper function to get the auth0Id
  return useUserMutation(API.postNewUser)
}

export function useDeleteUser() {
  return useUserMutation(API.deleteUser)
}
