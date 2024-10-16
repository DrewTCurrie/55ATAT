import { Box, Divider, Typography } from '@mui/material';
import React, {useEffect, useState} from 'react'

function Settings() {

    const [names, setNames] = useState([]);
    const [hasFetchedNames, setHasFetchedNames] = useState(false)
    useEffect(()=> {
      if(!hasFetchedNames) {
        const fetchNames = async () => {
          try {
            const response = await fetch(`/api/attendeeInitials`);
            const data = await response.json();
            setNames(data);
            setHasFetchedNames(true)
          } catch(e){
            console.error("Error fetching names:", e);
          }
        };
        fetchNames();
    }})

    return(
        <Box
        sx={{
          width: '100vw',
          height: '100vh',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: '#f0f0f0',
        }}>
            <Box
            sx={{
            padding: '2rem',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            minWidth: '300px',
            }}>
                <Typography variant='h5' component="h1" gutterBottom color='black'>Settings</Typography>
                <Divider/>
                <Box
                sx={{
                    my: '.4rem'
                }}>
                    <Typography variant='h6'>Default Settings</Typography>
                    
                </Box>
                <Divider/>
                <Box
                sx={{
                    my: '.4rem'
                }}>
                    <Typography variant='h6'>Attendee Settings</Typography>
                    
                </Box>
            </Box>
        </Box>
    );
};

export default Settings