import Sidebar from './components/sidebar'
import './App.css'
import Events from './pages/events'
import Clients from './pages/clients'
import { Routes, Route } from 'react-router-dom'
import { Box } from '@mui/material'
import React from 'react'
import Scanner from './pages/scanner'
import Login from './pages/login'
import AuthProvider from './funcitons/AuthProvider'
import ProtectedRoute from './funcitons/ProtectedRoute'
import Settings from './pages/settings'
import SettingsProvider from './funcitons/SettingsProvider'

function App() {
  return (
    <AuthProvider>
      <Box sx={{display: 'flex'}}>
        <Sidebar/>
        <SettingsProvider>
          <Routes>
            <Route path='settings' element={<Settings/>} />
          </Routes>
        </SettingsProvider>
        <Routes>
          <Route path='' element={<Scanner/>}/>
          <Route path='login' element={<Login/>}/>
          <Route element={<ProtectedRoute/>}>
            <Route path='events' element={<Events/>} />
          </Route>
          <Route element={<ProtectedRoute/>}>
            <Route path='clients' element={<Clients/>} />
          </Route>
          {/* <Route element={<ProtectedRoute/>}>
            <Route path='settings' element={<Settings/>} />
          </Route> */}
        </Routes>
      </Box>
    </AuthProvider>
  );
};

export default App
