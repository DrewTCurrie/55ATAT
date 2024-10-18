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
import AuthProvider from './funcitons/AuthProvider'
import ProtectedRoute from './funcitons/ProtectedRoute'

function App() {
  return (

function App() {
  return (
    <AuthProvider>
      <Box sx={{display: 'flex'}}>
        <Sidebar/>
        <Routes>
          <Route path='' element={<Scanner/>}/>
          <Route path='login' element={<Login/>}/>
          <Route element={<ProtectedRoute/>}>
            <Route path='events' element={<Events/>} />
          </Route>
          <Route element={<ProtectedRoute/>}>
            <Route path='clients' element={<Clients/>} />
          </Route>
          <Route element={<ProtectedRoute/>}>
            <Route path='settings' element={<Scanner/>} />
          </Route>
        </Routes>
      </Box>
    </AuthProvider>

  );
};

export default App
