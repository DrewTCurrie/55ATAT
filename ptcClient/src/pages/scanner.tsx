import { Button, Card, Grid2, TextField, Typography } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import { useSettings } from "../functions/SettingsProvider";
import { AudioPlayer } from "../components/audioPlayer";

//https://cdn.shopify.com/s/files/1/2144/8019/files/A5_Desktop_Scanner_User_Manual-V1.29.PDF?v=1706669102
//NETUM A5 Scanner will need to have the cariage return function set to automaticaly submit content


export default function Scanner(){
    //Initialize Audio Player
    const audioRef = useRef<HTMLAudioElement | null>(null);
    //This will replay the audio after input
    const playAudio = () => {
      if (audioRef.current) {
        audioRef.current.currentTime = 0;  // Reset to the start
        audioRef.current.play();           // Play the audio
      }
    };

    //Initialize Settings
    const settings = useSettings();
    //Scanner Data 
    const [scanData, setScanData] = useState('');
    //Handles input change from the textfield
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setScanData(event.target.value);
    };
    //When enter is pressed, either from user or scanner, start submit.
    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
      // If "Enter" key is pressed, submit the form
      if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission
        handleSubmit(); // Call the submit function
      }
    };

    //React Hook for handling submission
    const [loading, setLoading] = useState(false);
    //Input reference to refocus the input box after loading is false
    const inputRef = useRef<HTMLInputElement | null>(null);
    useEffect(() => {
      if (!loading && inputRef.current) {
        inputRef.current.focus();  // Refocus the text field when no longer loading
      }
    }, [loading]);

    const [eventSubmitted, setEventSubmitted] = useState(false);
    const [eventFailed, setEventFailed] = useState(false);
    const handleSubmit = async () => {
        console.log('Scanned Data Submitted:', scanData);
        let internalSubmit = false;
        let internalFail = false
        setLoading(true)
        const event = {
          method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
              "id": scanData
            })
          }
          try{
            const response = await fetch(`/api/scanEvent`,event)
            if (!response.ok) {
              internalFail = true
              throw new Error('Error creating Event');
            } else {
              internalSubmit = true
              setEventFailed(false)
              setEventSubmitted(true)
            }
          } catch(e){
            console.error("Error creating Event", e);
            setEventSubmitted(false)
            setEventFailed(true)
            setLoading(false)
          } finally {
            if(internalSubmit){
              settings?.getAttendeeMessage(scanData)
              settings?.getAttendeeAudio(scanData)
              //This waits for 1 second, before re-enabling
              await new Promise(f => setTimeout(f, 1000))
              playAudio()
            }
            if(internalFail){
              settings?.getFailureAudio()
              //This waits for 1 second, before re-enabling
              await new Promise(f => setTimeout(f, 1000))
              playAudio()
            }
            setLoading(false)
            closeMessages()
          }
        // Reset the input field if needed
        setScanData('');
    };
    //This will close messages after about 5 seconds.
    const closeMessages = async () => {
      await new Promise(f => setTimeout(f, 5000))
      setEventFailed(false)
      setEventSubmitted(false)
    }
    return(
        <>
        <Grid2
                display="flex" 
                flexDirection="column" 
                alignItems="center" 
                justifyContent="center"
                sx={{ minWidth: 300 }}
        >
          <Card>
            {!settings?.attendeeMessage ? 
            <Typography 
            variant="h2"
            sx={{my:'.8rem'}}>
              Welcome to PTC
            </Typography> 
            :
            <Typography 
            variant="h2"
            sx={{my:'.8rem'}}>
              {settings.attendeeMessage}</Typography> 
            }
            <TextField
            label="Scan Input"
            variant="outlined"
            fullWidth
            value={scanData}
            disabled={loading}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            autoFocus
            inputRef={inputRef}
            />
            <Button
              variant="contained"
              sx={{minWidth:300,my:'.4rem'}}
              disabled={loading}
              onClick={handleSubmit}>
              {loading ? 'Loading' :  'Submit Event'}</Button>
              {settings?.attendeeAudio && 
              <AudioPlayer audioUrl={settings.attendeeAudio} audioType={'audio/mpeg'} autoPlay={true}  audioRef={audioRef} />}
              {eventSubmitted ? <Typography color="green">Event Submitted Successfully</Typography> : ""}
              {eventFailed ? <Typography color="red">Event Submitted Unsuccessfully</Typography> : ""}
          </Card>
      </Grid2>
        </>
    );
}