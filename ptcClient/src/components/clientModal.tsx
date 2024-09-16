import { Autocomplete, Box, Button, Dialog, DialogTitle, Grid, TextField } from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import * as React from "react";

//TODO: create some error handling for this modal and the events modal


function ClientModal(){
  //handling the opening and closing of the modal.
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
      setOpen(false);
    };

    //useEffects loads the roles dropdown with roles from the database.
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
    //Hooks for name, username, pwd (if administrator). Usestate with string input.
    const [name, setName] = useState('')
    const [username, setUsername] = useState('')
    const [pwd, setPwd] = useState('')
    //Autocomplete Hook, sets the value based on input
    const [autoCompleteVal, setAutoCompleteVal] =  useState<{[key: string]: any}>({
      roleAutoComplete: []
    });
    const handleAutoCompleteChange = (name: string, newValue: any) => {
      setAutoCompleteVal((prevState) => ({
        ...prevState,
        [name]: newValue,
      }));
    }

    //Hook to check if role is employee or administrator (takes more jsx than the administrators field.)
    const employeeFieldVisibility = autoCompleteVal.roleAutoComplete.some(
      (role: string | string[]) => role.includes('Employee') || role === 'Administrator'
    );

    //Hook and handler to get file for employee picture
    const [file, setFile] = useState<File | null>(null)
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if(file){
        const fileType = file.type;
        if(fileType.startsWith('image/')){
          console.log(file);
          setFile(file);
        }
      }
    }


    const createAccount = async () => {};


    return(
    <Fragment>
        <Button onClick={handleClickOpen} >Create New Account </Button>
        <Dialog
            open={open}
            onClose={handleClose}>
            <DialogTitle align="center">Create New Account</DialogTitle>
            <Grid
              display="flex" 
              flexDirection="column" 
              alignItems="center" 
              justifyContent="center"
              sx={{ minWidth: 300 }}
            >
              <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                <TextField
                  required
                  sx={{minWidth: 300}}
                  label="Name (Initials)"
                  value={name}
                  onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setName(event.target.value);}}
                />
              </Box>
              <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                <Autocomplete
                  multiple
                  key="roleAutoComplete" 
                  sx={{minWidth: 300}}
                  options={roles}
                  value={autoCompleteVal.roleAutoComplete}
                  onChange={(_name: any, newValue: any) => handleAutoCompleteChange('roleAutoComplete', newValue)}
                  renderInput={(params) => <TextField {...params} label="Role" />}
                />
              </Box>
              {employeeFieldVisibility && (
                <>
                  <Box sx={{alignContent:'left',mb:'.6rem',mx:'.8rem'}}>
                    <label htmlFor="user_image">Upload Your Image:</label>
                  </Box>
                  <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                    <input 
                    type="file" 
                    id="user_image" 
                    name="user_image"
                    accept="image/png, image/jpeg, image/jpg, image/gif" 
                    onChange={handleFileChange}/>
                  </Box>
                </>
              )}
              {autoCompleteVal.roleAutoComplete.includes('Administrator') && (
              <>
                <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                  <TextField
                    sx={{minWidth: 300}}
                    label="Username"
                    value={username}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                      setUsername(event.target.value);}}
                  />
                </Box>
                <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                  <TextField
                  sx={{minWidth: 300}}
                  label="Password"
                  value={pwd}
                  onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setPwd(event.target.value);}}
                  />
                </Box>
              </>
              )}
              <Box sx={{mb:'.5rem'}}>
                <Button 
                  variant='contained'
                  onClick={createAccount}>Submit
                </Button>
              </Box>
            </Grid>
        </Dialog>
    </Fragment>
    )
}
export default ClientModal
