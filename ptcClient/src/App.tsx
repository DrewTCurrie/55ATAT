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

function App() {
  return (
    <AuthProvider>
      <Box sx={{display: 'flex'}}>
        <Sidebar/>
        <Routes>
          <Route path='' element={<Scanner/>}/>
          <Route path='login' element={<Login/>}/>
          <Route path='events' element={<Events/>} />
          <Route path='clients' element={<Clients/>} />
        </Routes>
      </Box>
    </AuthProvider>
  );
};

export default App
