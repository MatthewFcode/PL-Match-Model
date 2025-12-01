import { useAuth0 } from '@auth0/auth0-react'

export const useIsAuthenticated = () => {
  const { isAuthenticated, isLoading } = useAuth0()
  return { isAuthenticated, isLoading }
}

interface Props {
  children: React.ReactNode
}
export function IfAuthenticated({ children }: Props) {
  const { isAuthenticated, isLoading } = useIsAuthenticated()

  if (isLoading) return null
  return isAuthenticated ? <>{children}</> : null
}

export function IfNotAuthenticated({ children }: Props) {
  const { isAuthenticated, isLoading } = useIsAuthenticated()

  if (isLoading) return null
  return !isAuthenticated ? <>{children}</> : null
}
