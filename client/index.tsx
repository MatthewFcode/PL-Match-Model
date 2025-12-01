import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { RouterProvider } from 'react-router/dom'
import { createBrowserRouter } from 'react-router'
import { Auth0Provider } from '@auth0/auth0-react'
import routes from './routes.tsx'

const queryClient = new QueryClient()

const router = createBrowserRouter(routes)

document.addEventListener('DOMContentLoaded', () => {
  createRoot(document.getElementById('app') as HTMLElement).render(
    <Auth0Provider
      domain="dev-qh0h6ps1a3nl4n4w.au.auth0.com"
      clientId="h1CYomLgZfJsruXgawpnwZeGEmI6Gemv"
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: 'https://match-model/api',
      }}
    >
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
        <ReactQueryDevtools />
      </QueryClientProvider>
    </Auth0Provider>,
  )
})
