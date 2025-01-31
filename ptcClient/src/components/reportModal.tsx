import { Autocomplete, Box, Button, Checkbox, Dialog, DialogTitle, TextField } from "@mui/material";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { Fragment, useEffect, useState } from "react";
import * as React from "react"; 
import axios from 'axios'

function ReportModal(){
    //Open React Hook
    const [open, setOpen] = useState(false);
    //Open and Close handler
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
      setOpen(false);
    };

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

    //Date Hooks
    const [startDate, setStartDate]=useState(null);
    const [endDate, setEndDate]=useState(null);
    
    //Checkbox hook, identifies which checkbox then changes it
    const [isChecked, setIsChecked] = useState<{ [key: string]: boolean }>({
      nameCheckbox: false,
      roleCheckbox: false,
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
      nameAutoComplete: null,
      roleAutoComplete: null
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
            "startDate": startDate,
            "endDate": endDate
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
        if(!response.ok){
          throw new Error(`Error: ${response.statusText}`);
        }  
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
              key="roleAutoComplete" 
              sx={{ width: 300 }}
              options={roles} 
              disabled={!isChecked.roleCheckbox} 
              onChange={(_name: any, newValue: any) => handleAutoCompleteChange('roleAutoComplete', newValue)}
              value={autoCompleteVal.roleAutoComplete}
              renderInput={(params) => <TextField {...params} label="Role" />}/>
          </Box>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker 
                label="Start Date" 
                sx={{mb:'.5rem',mx:'.8rem'}}
                value={startDate}
                onChange={(newDate: any)=> setStartDate(newDate)}
                maxDate={endDate}
                />
            </LocalizationProvider>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker 
                label="End Date" 
                sx={{mb:'.5rem',mx:'.8rem'}} 
                value={endDate}
                onChange={(newDate: any)=> setEndDate(newDate)}
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