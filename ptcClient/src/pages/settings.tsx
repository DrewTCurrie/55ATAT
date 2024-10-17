import { Autocomplete, Box, Button, Divider, TextField, Typography } from '@mui/material';
import React, {useEffect, useState} from 'react'
import { useSettings } from '../funcitons/SettingsProvider';

function Settings() {
    //Initialize Setting Provides as setttings
    const settings = useSettings();
    //Gets Names of Attendees in Database for Personalized Messasges.
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
        }
    })
    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);


    /**
     * Default GETS/SETS
     */
    //This will handle the submission of a default message.
    const submitDefaultMessage = () => {
        setLoading(true)
        settings?.setDefaultMessage(settings?.defaultMessage)
        setLoading(false)
    }
    const resetDefaults = () =>{
        setLoading(true)
        settings?.resetDefaults()
        setLoading(false)
    }

    /**
     * ATTENDEE GETS/SETS
     */


    //This handles selecting an attendee from the attendee list
    const [selectedAttendee, setSelectedAttendee] = useState('')
    const [attendeeSelected, isAttendeeSelected] = useState(false)
    const handleSelectAttendee = (attendee: string) =>{
        setSelectedAttendee(attendee)
        settings?.getAttendeeMessage(attendee)
        isAttendeeSelected(true)
    }

    //This will handle the submission of a attendee message
    const submitAttendeeMessage = () => {
        setLoading(true)
        settings?.setAttendeeMessage(selectedAttendee, settings?.attendeeMessage)
        setLoading(false)
    }
    //This will handle the reseting of an attendee
    const resetAttendee = () =>{
        setLoading(true)
        settings?.resetAttendee(selectedAttendee)
        setLoading(false)
    }

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
                    <Box>
                        <TextField
                            label="Default Message"
                            name="defaultmessage"
                            variant="outlined"
                            fullWidth
                            multiline
                            value={settings?.defaultMessage}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                settings?.setDMessage(event.target.value);}}
                            sx={{
                                my: '.4rem'
                            }}
                        />
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            fullWidth
                            sx={{ mb:'.4rem' }}
                            disabled={loading}
                            onClick={submitDefaultMessage}
                        >
                            {loading ? 'Loading' : 'Update Message'}
                        </Button>
                        <Button
                            type="submit"
                            variant="contained"
                            color="error"
                            fullWidth
                            sx={{ my:'.4rem' }}
                            disabled={loading}
                            onClick={resetDefaults}
                        >
                            {loading ? 'Loading' : 'Reset Default Settings'}
                        </Button>
                    </Box>
                </Box>
                <Divider/>
                <Box
                sx={{
                    my: '.4rem'
                }}>
                    <Typography variant='h6'>Attendee Settings</Typography>
                    <Box>
                    <Autocomplete 
                        key="nameAutoComplete"
                        options={names} 
                        onChange={(_event: any, newValue: any) => handleSelectAttendee(newValue)}
                        value={selectedAttendee}
                        fullWidth
                        renderInput={(params: any) => <TextField {...params} label="Name (Initials)" />}
                        sx={{
                            my: '.4rem'
                        }}/>
                        {attendeeSelected ? 
                        <Box>
                        <TextField
                            label={`${selectedAttendee}'s Message`}
                            name="defaultmessage"
                            variant="outlined"
                            fullWidth
                            multiline
                            value={settings?.attendeeMessage}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                settings?.setAMessage(event.target.value);}}
                            sx={{
                                my: '.4rem'
                            }}
                        />
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            fullWidth
                            sx={{ my:'.4rem' }}
                            disabled={loading}
                            onClick={submitAttendeeMessage}
                        >
                            {loading ? 'Loading' : 'Update Message'}
                        </Button>
                        <Button
                            type="submit"
                            variant="contained"
                            color="error"
                            fullWidth
                            sx={{ my:'.4rem' }}
                            disabled={loading}
                            onClick={resetAttendee}
                        >
                            {loading ? 'Loading' : 'Reset Attendee Settings'}
                        </Button>
                        </Box>
                        : ''}
                    </Box>    
                </Box>
            </Box>
        </Box>
    );
};

export default Settings