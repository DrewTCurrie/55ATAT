import Sidebar from './components/sidebar'
import './App.css'
import Events from './pages/events'
import Clients from './pages/clients'
import { Routes, Route } from 'react-router-dom'
import { Box } from '@mui/material'
import React from 'react'
import Scanner from './pages/scanner'
import Table from './components/table'

import Login from './pages/login'
import AuthProvider from './functions/AuthProvider'
import ProtectedRoute from './functions/ProtectedRoute'
import Settings from './pages/settings'
import SettingsProvider from './functions/SettingsProvider'

function App() {
  return (
    <AuthProvider>
      <Box sx={{display: 'flex'}}>
        <Sidebar/>
          <Routes>
          <Route path='' element={<SettingsProvider><Scanner/></SettingsProvider>}/>
          <Route path='login' element={<Login/>}/>
          <Route element={<ProtectedRoute/>}>
            <Route path='events' element={<Events/>} />
          </Route>
          <Route element={<ProtectedRoute/>}>
            <Route path='clients' element={<Clients/>} />
          </Route>
          <Route element={<ProtectedRoute/>}>
            <Route path='settings' element={<SettingsProvider><Settings/></SettingsProvider>} />
          </Route>
        </Routes>
      </Box>
    </AuthProvider>

  );
};

export default App
