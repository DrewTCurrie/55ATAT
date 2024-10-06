import Sidebar from './components/sidebar'
import './App.css'
import Events from './pages/events'
import Clients from './pages/clients'
import { Routes, Route } from 'react-router-dom'
import { Box } from '@mui/material'
import React from 'react'
import Scanner from './pages/scanner'

function App() {
  return (
    <Box sx={{display: 'flex'}}>
      <Sidebar/>
      <Routes>
        <Route path='' element={<Scanner/>}/>
        <Route path='events' element={<Events/>} />
        <Route path='clients' element={<Clients/>} />
      </Routes>
    </Box>
  );
};

export default App
