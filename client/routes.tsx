/* eslint-disable react/jsx-key */
import { createRoutesFromElements, Route } from 'react-router'
import App from './components/App'
import Model from './components/Model.tsx'

const routes = createRoutesFromElements(
  <>
    <Route index element={<App />} />
    <Route path="/model" element={<Model />} />
  </>,
)

export default routes
