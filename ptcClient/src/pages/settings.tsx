import { Autocomplete, Box, Button, Divider, TextField, Typography } from '@mui/material';
import React, {useEffect, useRef, useState} from 'react'
import { useSettings } from '../functions/SettingsProvider';
import { AudioPlayer } from '../components/audioPlayer';

interface Attendee {
    ID: string;
    Initials: string;
}

function Settings() {
    //Initialize Audio Player
    const audioRef = useRef<HTMLAudioElement | null>(null);
    //Initialize Setting Provides as setttings
    const settings = useSettings();
    //Gets Names of Attendees in Database for Personalized Messasges.
    const [names, setNames] = useState<{ Initials: string; ID: string }[]>([]);
    const [hasFetchedNames, setHasFetchedNames] = useState(false)

    useEffect(()=> {
      if(!hasFetchedNames) {
        const fetchNames = async () => {
          try {
            const response = await fetch(`/api/getAttendeeInitialsAndID`);
            const data: Attendee[]  = await response.json();
            // Map data to the format needed by Autocomplete
            const formattedNames = data.map(attendee => ({
                Initials: attendee.Initials,  // Label for display
                ID: attendee.ID         // Value for identification
            }));
            setNames(formattedNames);
            setHasFetchedNames(true);
          } catch(e){
            console.error("Error fetching names:", e);
          }
        };
            fetchNames();
        }
    },[hasFetchedNames])
    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);


    /**
     * Default GETS/SETS
     */
    //This will handle the submission of a default message.
    const submitDefaultMessage = async () => {
        setLoading(true)
        settings?.setDefaultMessage(settings?.defaultMessage)
        setLoading(false)
        
    }
    //This resets the default settings
    const resetDefaults = () =>{
        setLoading(true)
        settings?.resetDefaults()
        setLoading(false)
    }

    //This handles the uploading of files to the webpage
    const [selectedFile, setSelectedFile] = useState<File>();
    const [audioSrc, setAudioSrc] = useState('');
    const [fileName, setFileName] = useState("")
    const [audioType, setAudioType] = useState("")
    const handleDefaultAudioChange = (event: any) => {
        setLoading(true)
        //revoke prior urls
        const file = event.target.files[0];
        URL.revokeObjectURL(file)
        setAudioSrc('')
        if(file){
            const fileType = file.type 
            if(fileType.startsWith('audio/')){
                //Set Player audio Type
                setAudioType(fileType)
                //Set audio File and audio file name.
                setSelectedFile(file);
                setFileName(file ? file.name : "");
                //allow for local playback by creating a url for audio player source.
                const tempAudioURL = URL.createObjectURL(file);
                setAudioSrc(tempAudioURL)
            }
        }
        setLoading(false)
    }

    //This will handle the submission of default audioFile
    const submitDefaultAudio = () => {
        setLoading(true)
        if(selectedFile){
            settings?.setDefaultAudio(selectedFile)
        }
        setLoading(false)
    }

    /**
     * ATTENDEE GETS/SETS
     */


    //This handles selecting an attendee from the attendee list
    const [selectedAttendee, setSelectedAttendee] = useState<Attendee>();
    const [attendeeSelected, isAttendeeSelected] = useState(false)
    const handleSelectAttendee = (attendee: Attendee) =>{
        if(attendee){
            setSelectedAttendee(attendee)
            settings?.getAttendeeMessage(attendee.ID)
            settings?.getAttendeeAudio(attendee.ID)
            isAttendeeSelected(true)
        } else {
            isAttendeeSelected(false)
        }

    }

    //This will handle the submission of a attendee message
    const submitAttendeeMessage = () => {
        setLoading(true)
        if(selectedAttendee){
            settings?.setAttendeeMessage(selectedAttendee.ID, settings?.attendeeMessage)
        }    
        setLoading(false)
    }
    //This will handle the reseting of an attendee
    const resetAttendee = () =>{
        setLoading(true)
        console.log(selectedAttendee)
        if(selectedAttendee){
            settings?.resetAttendee(selectedAttendee.ID)
        }
        setLoading(false)
    }

    //This handles the uploading of attendee audio to the webpage
    const [selectedAttendeeFile, setSelectedAttendeeFile] = useState<File>();
    const [attendeeAudioSrc, setAttendeeAudioSrc] = useState('');
    const [attendeeFileName, setAttendeeFileName] = useState("")
    const [attendeeAudioType, setAttendeeAudioType] = useState("")
    const handleAttendeeAudioChange = (event: any) => {
        setLoading(true)
        //revoke prior urls
        const file = event.target.files[0];
        URL.revokeObjectURL(file)
        setAttendeeAudioSrc('')
        if(file){
            const fileType = file.type 
            if(fileType.startsWith('audio/')){
                //Set Player audio Type
                setAttendeeAudioType(fileType)
                //Set audio File and audio file name.
                setSelectedAttendeeFile(file);
                setAttendeeFileName(file ? file.name : "");
                //allow for local playback by creating a url for audio player source.
                const tempAudioURL = URL.createObjectURL(file);
                setAttendeeAudioSrc(tempAudioURL)
            }
        }
        setLoading(false)
    }

    //This will handle the submission of default audioFile
    const submitAttendeeAudio = async () => {
        try{
        setLoading(true)
            if(selectedAttendeeFile && selectedAttendee){
            await settings?.setAttendeeAudio(selectedAttendee.ID, selectedAttendeeFile)
            } else {
                throw new Error('No attendee audio selected')
            }
        } catch(e){
            console.error("Error submitting attendee Audio:", e)
        } finally {
            setLoading(false)
        }
        
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
                            {settings?.defaultAudio && !audioSrc && (
                                <div>
                                    <audio controls>
                                        <source src={settings?.defaultAudio} type='audio/mpeg' />
                                        Your browser does not support the audio element.
                                    </audio>
                                </div>
                            )}
                            {audioSrc && (
                                
                                <div>
                                    <AudioPlayer audioUrl={audioSrc} audioType={audioType} audioRef={audioRef}/>
                                </div>
                            )}
                            {fileName && (
                                <Typography
                                sx={{mt:'.4rem'}}>
                                    File name: {fileName}
                                </Typography>
                            )}
                            <Box>
                            <input
                                accept="audio/*"
                                style={{ display: 'none' }}
                                id="audio-upload"
                                type="file"
                                onChange={handleDefaultAudioChange}
                            />
                            <label htmlFor="audio-upload">
                                <Button 
                                    variant="contained"
                                    component="span"
                                    color="secondary"
                                    fullWidth
                                    sx={{ my:'.2rem' }}
                                    disabled={loading}>
                                    Select Audio File
                                </Button>
                            </label>
                            {audioSrc ?                         
                                <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                fullWidth
                                sx={{ my:'.2rem' }}
                                disabled={loading}
                                onClick={submitDefaultAudio}
                                >
                                    {loading ? 'Loading' : 'Update Audio'}
                                </Button> : ''}
                            </Box>
                        <Button
                            type="submit"
                            variant="contained"
                            color="error"
                            fullWidth
                            sx={{ my:'.2rem' }}
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
                        getOptionLabel={(option) => option.Initials}
                        onChange={(_event: any, newValue: any) => handleSelectAttendee(newValue)}
                        value={selectedAttendee}
                        fullWidth
                        renderInput={(params: any) => <TextField {...params} label="Name (Initials)" />}
                        sx={{
                            my: '.4rem'
                        }}
                        isOptionEqualToValue={(option, value) => option.ID === value?.value}/>
                        {attendeeSelected ? 
                        <Box>
                        <TextField
                            label={`${selectedAttendee?.Initials}'s Message`}
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
                            {loading ? 'Loading' : `Update ${selectedAttendee?.Initials}'s Message`}
                        </Button>
                        {settings?.attendeeAudio && !attendeeAudioSrc && (
                                <div>
                                    <AudioPlayer audioUrl={settings?.attendeeAudio} audioType='audio/mpeg' audioRef={audioRef}/>
                                </div>
                            )}
                            {attendeeAudioSrc && (
                                
                                <div>
                                    <AudioPlayer audioUrl={attendeeAudioSrc} audioType={attendeeAudioType}  audioRef={audioRef}/>
                                </div>
                            )}
                            {attendeeFileName && (
                                <Typography
                                sx={{mt:'.4rem'}}>
                                    File name: {attendeeFileName}
                                </Typography>
                            )}
                            <Box>
                            <input
                                accept="audio/*"
                                style={{ display: 'none' }}
                                id="attendee-audio-upload"
                                type="file"
                                onChange={handleAttendeeAudioChange}
                            />
                            <label htmlFor="attendee-audio-upload">
                                <Button 
                                    variant="contained"
                                    component="span"
                                    color="secondary"
                                    fullWidth
                                    sx={{ my:'.2rem' }}
                                    disabled={loading}>
                                    Select Audio File
                                </Button>
                            </label>
                            {attendeeAudioSrc ?                         
                                <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                fullWidth
                                sx={{ my:'.2rem' }}
                                disabled={loading}
                                onClick={submitAttendeeAudio}
                                >
                                    {loading ? 'Loading' : `Update ${selectedAttendee?.Initials}'s Audio`}
                                </Button> : ''}
                            </Box>
                        <Button
                            type="submit"
                            variant="contained"
                            color="error"
                            fullWidth
                            sx={{ my:'.4rem' }}
                            disabled={loading}
                            onClick={resetAttendee}
                        >
                            {loading ? 'Loading' :  `Reset ${selectedAttendee?.Initials}'s Settings`}
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