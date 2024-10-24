import { Autocomplete, Box, Button, Checkbox, Dialog, DialogTitle, TextField } from "@mui/material";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { Fragment, useEffect, useState } from "react";
import * as React from "react"; 
import axios from 'axios'
import dayjs from "dayjs";
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc);
dayjs.extend(timezone);

function ReportModal(){
    //Open React Hook
    const [open, setOpen] = useState(false);
    //Open and Close handler
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
      handleAutoCompleteChange('roleAutoComplete', [])
      handleAutoCompleteChange('nameAutoComplete', [])
      setIsChecked({
        nameCheckbox: false,
        roleCheckbox: false,
        eventTypeCheckBox: false,
      });
      setStartDate(dayjs())
      setEndDate(dayjs())
      setOpen(false);
    };
    //Get the Roles in the database, and present them in autocomplete boxes
    const [roles, setRoles] = useState([]);
    const [hasFetchedRoles, setHasFetchedRoles] = useState(false)
    useEffect(()=> {
      if(open && !hasFetchedRoles) {
        const fetchRoles = async () => {
          try {
            const response = await fetch(`/api/getRoles`);
            const data = await response.json();
            setRoles(data);
            setHasFetchedRoles(true)
          } catch(e){
            console.error("Error fetching roles:", e);
          }
        };
        fetchRoles();
    }})
    //Get names (attendee initials) in the database, and present them for choice.
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

    //Setup the couple attendance event types.
    const eventTypes = [ 'Present', 'Absent','TIL'];

    //Date Hooks
    const [startDate, setStartDate]=useState(dayjs());
    const [endDate, setEndDate]=useState(dayjs());
    
    //Checkbox hook, identifies which checkbox then changes it
    const [isChecked, setIsChecked] = useState<{ [key: string]: boolean }>({
      nameCheckbox: false,
      roleCheckbox: false,
      eventTypeCheckBox: false,
    });
    //Checkbox Handler
    const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const { name, checked} = event.target;
      setIsChecked((prevState) => ({
        ...prevState,
        [name]: checked,
      }));
    };

    //Autocomplete Hook, works the same as the Checkbox, but with different value content.
    const [autoCompleteVal, setAutoCompleteVal] =  useState<{[key: string]: any}>({
      nameAutoComplete: [],
      roleAutoComplete: [],
      eventTypeAutoComplete: [],
    });
    const handleAutoCompleteChange = (name: string, newValue: any) => {
      setAutoCompleteVal((prevState) => ({
        ...prevState,
        [name]: newValue,
      }));
    }

    const generateReport = async () => {
      //JSON for a quick report, (7 days back)
      const report = { 
          method: 'POST',
          headers: {'Content-Type': 'application/json',},
          body: JSON.stringify({
            "name": autoCompleteVal.nameAutoComplete,
            "role": autoCompleteVal.roleAutoComplete,
            "eventType": autoCompleteVal.eventTypeAutoComplete,
            "startDate": startDate.tz("America/Denver").format("YYYY-MM-DDTHH:mm:ss.SSS[Z]"),
            "endDate": endDate.tz("America/Denver").format("YYYY-MM-DDTHH:mm:ss.SSS[Z]")
          })}
      //Try 
      console.log(report)
      try {
        const response = await fetch(`/api/generateReport`, report).then(
          res => res.json()
        ).then(
           data => {
            axios.get(`/api/download/${data}`,{responseType: 'blob'}
            ).then((downloadRes) => {
              const url = window.URL.createObjectURL(new Blob([downloadRes.data]));
              const link = document.createElement('a');
              link.href=url;
              link.setAttribute('download',`${data}`);
              document.body.appendChild(link);
              link.click();
            })
          }
        );
      } catch(e: any){
        console.log(e.message);
      }
    };

    return(
    <Fragment>
        <Button onClick={handleClickOpen} >Generate Custom Report</Button>
        <Dialog
          open={open}
          onClose={handleClose}>
          <DialogTitle align="center">Generate Custom Report</DialogTitle>
          <Box display="flex" sx={{mb:'.4rem',mx:'.8rem'}}>
            <Checkbox 
              name="nameCheckbox"
              checked={isChecked.nameCheckbox}
              onChange={handleCheckboxChange}/>
            <Autocomplete 
              multiple
              key="nameAutoComplete"
              sx={{ width: 300 }}
              options={names} 
              disabled={!isChecked.nameCheckbox}
              onChange={(_name: any, newValue: any) => handleAutoCompleteChange('nameAutoComplete', newValue)}
              value={autoCompleteVal.nameAutoComplete}
              renderInput={(params) => <TextField {...params} label="Name (Initials)" />}/>
          </Box>
          <Box display="flex" sx={{mb:'.6rem',mx:'.8rem'}}>
            <Checkbox 
              name="roleCheckbox"
              checked={isChecked.roleCheckbox}
              onChange={handleCheckboxChange}/>
            <Autocomplete
              multiple
              key="roleAutoComplete" 
              sx={{ width: 300 }}
              options={roles} 
              disabled={!isChecked.roleCheckbox} 
              onChange={(_name: any, newValue: any) => handleAutoCompleteChange('roleAutoComplete', newValue)}
              value={autoCompleteVal.roleAutoComplete}
              renderInput={(params) => <TextField {...params} label="Role" />}/>
          </Box>
          <Box display="flex" sx={{mb:'.6rem',mx:'.8rem'}}>
            <Checkbox 
              name="eventTypeCheckBox"
              checked={isChecked.eventTypeCheckBox}
              onChange={handleCheckboxChange}/>
            <Autocomplete
              multiple
              key="roleAutoComplete" 
              sx={{ width: 300 }}
              options={eventTypes} 
              disabled={!isChecked.eventTypeCheckBox} 
              onChange={(_name: any, newValue: any) => handleAutoCompleteChange('eventTypeAutoComplete', newValue)}
              value={autoCompleteVal.eventTypeAutoComplete}
              renderInput={(params) => <TextField {...params} label="Event Type" />}/>
          </Box>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker 
                label="Start Date" 
                sx={{mb:'.5rem',mx:'.8rem'}}
                value={startDate}
                onChange={(newDate: any)=> setStartDate(dayjs(newDate).startOf('day'))}
                maxDate={endDate}
                />
            </LocalizationProvider>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker 
                label="End Date" 
                sx={{mb:'.5rem',mx:'.8rem'}} 
                value={endDate}
                onChange={(newDate: any)=> setEndDate(dayjs(newDate).endOf('day'))}
                minDate={startDate}
                />
            </LocalizationProvider>
            <Box display="center" sx={{mb:'.5rem'}}>
              <Button 
                variant='contained'
                onClick={generateReport}>Submit</Button>
            </Box>
        </Dialog>
    </Fragment>
    )
} 
export default ReportModal