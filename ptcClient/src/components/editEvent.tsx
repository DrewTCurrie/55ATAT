import { Autocomplete, Box, Button, Checkbox, Dialog, DialogTitle, FormControlLabel, Grid2, IconButton, Stack, TextField } from '@mui/material';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { DateTimePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import EditIcon from '@mui/icons-material/Edit';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

interface modalProps{
    onClose: () => void;
    EventID: string;
    Initials: string;
    Timestamp: string;
    Absent: boolean;
    TIL: boolean;
    AdminInitials: string;
    Comment: string;
}

dayjs.extend(utc);
dayjs.extend(timezone);

export default function EditEvent({onClose,EventID,Initials,Timestamp,Absent,TIL,AdminInitials,Comment}:modalProps){
    //Handling the open and closing of edit modal
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
        //Autofill details from the table
        handleAutoCompleteChange('nameAutoComplete', Initials)
        setIsChecked(prevState => ({
            ...prevState,
            tailCheckbox: TIL,
            absentCheckbox: Absent
          }));
        setComment(Comment)
        setOpen(true);
    };
    const handleClose = () => {
        //Clear values in form
        handleAutoCompleteChange('nameAutoComplete', '');
        setDate(dayjs());
        setIsChecked(prevState => ({
            ...prevState,
            tailCheckbox: false,
            absentCheckbox: false
          }));
        setComment('');
        //Refresh Table
        onClose();
        //Close modal and reset submission
        setEventSubmitted(false);
        setOpen(false);
    }
    //Hook for selecting a user name from autocomplete
    //Autocomplete Hook, works the same as the Checkbox, but with different value content.
    const [autoCompleteVal, setAutoCompleteVal] =  useState<{[key: string]: any}>({
        nameAutoComplete: null,
        roleAutoComplete: null
    });
    const handleAutoCompleteChange = (name: string, newValue: any) => {
    setAutoCompleteVal((prevState) => ({
        ...prevState,
        [name]: newValue,
    }));
    }
    
    //Date Hooks
    const [date, setDate]=useState(dayjs(Timestamp));
    //Hook for Comment
    const [comment, setComment] = useState('');
    //Checkbox hook, identifies which checkbox then changes it
    const [isChecked, setIsChecked] = useState<{ [key: string]: boolean }>({
        tailCheckbox: false,
        absentCheckbox: false,
        });
        //Checkbox Handler
        const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, checked} = event.target;
        setIsChecked((prevState) => ({
            ...prevState,
            [name]: checked,
        }));
        };

    /**
    * Loading Data in to the modal (Names Only)
    */
    //Hook to populate user drop down (blank = placeholder/no name) 
    const [names, setNames] = useState([]);
    const [hasFetchedNames, setHasFetchedNames] = useState(false)
    useEffect(()=> {
      if(open && !hasFetchedNames) {
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
    
    /**
    * Event Creation handler, this calls createEvent with appropriate information.
    */
    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);

    //Hook to check for event submission
    const [eventSubmitted, setEventSubmitted] = useState(false)
    const createEvent = async () => {
        //Set Loading to True to disable button
        setLoading(true)
        //create the event JSON
        const event = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                eventid: EventID,
                initials: autoCompleteVal.nameAutoComplete,
                date: date.tz("America/Denver").format("YYYY-MM-DDTHH:mm:ss.SSS[Z]"),
                tail: isChecked.tailCheckbox,
                absence: isChecked.absentCheckbox,
                comment: comment
            })
        }
        //try catch to query backend
        try{
            const response = await fetch(`/api/editEvent`,event);
            if (!response.ok) {
              throw new Error('Error creating event');
            } else {
                setEventSubmitted(true)
                setLoading(false)
            }
        } catch(e){
            console.error("Error creating event",e)
            setLoading(false)
        }
    }
    return(
        <>
        <IconButton 
                onClick={handleClickOpen}
                aria-label='edit'>
                <EditIcon/>
            </IconButton>
        <Dialog
        open={open}
        onClose={handleClose}>
            <DialogTitle align='center'>Edit Attendance Event</DialogTitle>
            <Grid2
                display="flex" 
                flexDirection="column" 
                alignItems="center" 
                justifyContent="center"
                sx={{ minWidth: 300 }}>
            <Box 
                display="flex" 
                sx={{mb:'.4rem',mx:'.8rem'}}>
                <Autocomplete 
                key="nameAutoComplete"
                sx={{ minWidth: 300 }}
                options={names} 
                onChange={(_name: any, newValue: any) => handleAutoCompleteChange('nameAutoComplete', newValue)}
                value={autoCompleteVal.nameAutoComplete}
                renderInput={(params) => <TextField {...params} label="Name (Initials)" />}/>
            </Box>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DateTimePicker 
                label="Date & Time (Blank for Current)" 
                sx={{mb:'.5rem',mx:'.8rem', mt:'.4rem', minWidth: 300}} 
                value={date}
                onChange={(newDate: any)=> setDate(dayjs(newDate))}
                />
            </LocalizationProvider>
            <Box display="flex" sx={{mb:'.6rem',mx:'.8rem'}}>
            <FormControlLabel
            control={
                <Checkbox              
                name="tailCheckbox"
                checked={isChecked.tailCheckbox}
                onChange={handleCheckboxChange}/>}
            label = 'TAIL Violation?'
            />
            <FormControlLabel
            control={
                <Checkbox              
                name="absentCheckbox"
                checked={isChecked.absentCheckbox}
                onChange={handleCheckboxChange}/>}
            label = 'Unexcused Absence?'
            />               
            </Box>
            {(isChecked.tailCheckbox || isChecked.absentCheckbox ) && (
                <TextField
                sx={{minWidth:300}}
                multiline
                label='Comment'
                value={comment}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setComment(event.target.value);}}/>
            )}
            </Grid2>
            <Stack 
            direction="row"
            display="flex" 
            alignItems="center" 
            justifyContent="center"
            spacing={4}
            sx={{mb:'.6rem',mt:'.4rem',mx:'.4rem'}}>
                <Button 
                    variant='outlined'
                    disabled={loading}
                    onClick={createEvent}>
                        {loading ? 'Loading' : eventSubmitted ? 'Event Edited Successfully' : 'Submit Event'}
                </Button>
                <Button
                    variant='contained'
                    onClick={() => {handleClose(); onClose()}}
                    disabled={loading}>
                        Close
                </Button>
            </Stack>
        </Dialog>
        </>
    )
}