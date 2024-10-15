import * as React from 'react'
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import { useEffect, useState } from 'react';
import { Autocomplete, Box, Button, Dialog, DialogTitle, Grid2, Stack, TextField } from '@mui/material';
interface badgeRespone {
    front: String,
    back?: String
  }

interface modalProps{
  onClose: () => void;
  ID: string,
  Initials: string,
  Roles: string | string[]
}

 export default function EditAttendee({onClose,ID,Initials,Roles}: modalProps){
    //Handling the open and closing of edit modal
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      //Autofill details from the table
      handleAutoCompleteChange('roleAutoComplete',Roles)
      setName(Initials)
      setOpen(true);
    };
    const handleClose = () => {
      //Refresh Table
      onClose()
      //Clear all values in form
      setName('')
      setUsername('')
      setPwd('')
      setBadgeURLs(null)
      //Close modal
      setOpen(false);
      setDisplayBadge(false)
    }
    //Hook for handling going back from the print screen
    const handleBack = () => {
        setDisplayBadge(false);
    }

    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);

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

    /*
    * Hook and handler to get file for employee picture
    */
    const [file, setFile] = useState<File>()
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

    //Hooks for handling badge displaying
    const [displayBadge, setDisplayBadge] = useState(false);
    const [badgeURLs, setBadgeURLs] =  useState<badgeRespone | null>();
    //Calls the backend to get a user's badge
    const loadBadge = async () => {
        //Attempt to generate a badge for the user.
        const badgeDetails = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                "userID": ID
        })
        }
        try{
            const badgeResponse = await fetch(`/api/generateBadge`,badgeDetails)
            if (!badgeResponse.ok) {
            throw new Error('Error creating User Badge');
            }
            const data = await badgeResponse.json();
            setBadgeURLs(data);
            setDisplayBadge(true);
            setLoading(false);
        } catch(e){
            console.error("Error creating account", e);
            setLoading(false)
      }
    }
    /*
    * Account Editing Handler, calls editAccount, then uses the ID to edit an administrator if either is updated
    */
    const editAccount = async () => {
      //Set Loading to True to disable button
      setLoading(true)
      //Create form data for accountData
      const accountData = new FormData();
      accountData.append('id',ID);
      accountData.append('name',name);
      accountData.append('roles',JSON.stringify(autoCompleteVal.roleAutoComplete))
      //Check if a file exists, if true append.
      if(file){
        accountData.append('file', file)
      }
      const account = {
        method: 'POST',
        body: accountData
      }
      try{
        const response = await fetch(`/api/editAccount`,account);
        if (!response.ok) {
          throw new Error('Error creating account');
        }
        //If the user account is an administrator, attempt to edit the administrator
        if(autoCompleteVal.roleAutoComplete.includes('Administrator')){
          const adminAccount = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
              "adminID": ID,
              "username": username,
              "password": pwd
            })
          }
          const adminResponse = await fetch(`/api/editAdmin`,adminAccount)
          if (!adminResponse.ok) {
            throw new Error('Error creating Administrator Account');
          }
        }
        setLoading(false);
      } catch(e){
        console.error("Error editing account", e);
        setLoading(false)
      }
    }

    /*
    * Print handler, will create a new window with only the pictures to print.
    */
    const handlePrint = () => {
        const printWindow = window.open('','_blank');
        if(printWindow){
            printWindow.document.write(`
            <html>
                <head>
                <title>Print</title>
                </head>
                <style>
                @media print {
                    body {
                    margin: 0;
                    padding: 0;
                    }
                    .page {
                    page-break-after: always; /* Ensure each image goes to a new page */
                    text-align: center;
                    }
                    img {
                    max-width: 100%;
                    height: 100%;
                    display: block;
                    margin: 0 auto;
                    }
                }
                </style>
                <body>
                <div class="page">
                    <img src="${badgeURLs?.front}" alt="Output 1" />
                </div>
                ${badgeURLs?.back ? (`
                <div class="page">
                    <img src=${badgeURLs.back} alt="Output 2" />
                </div>
                `):''}
                </body>
            </html>`);
        printWindow.document.close();
        printWindow.print();
        }
    }
    //Making the output images more viewable
    const scrollableContentStyle: React.CSSProperties = {
        maxHeight: '400px', // Set a max height for the scrollable area
        overflowY: 'auto', // Enable vertical scrolling
        marginBottom: '16px', // Space between images and buttons
      };
  

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
                <DialogTitle align='center'>Edit Account</DialogTitle>
            {!displayBadge ? ( 
            <>
            <Grid2
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
                    inputProps={{ maxLength: 8 }}
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
              </Grid2>
            <Grid2>
                <Grid2
                display="flex" 
                flexDirection="column" 
                alignItems="center" 
                justifyContent="center"
                sx={{ minWidth: 300 }}>
                    
                </Grid2>
                <Stack 
                direction="row"
                display="flex" 
                alignItems="center" 
                justifyContent="center"
                spacing={4}
                sx={{mb:'.6rem'}}>
                    <Button
                    variant='contained'
                    color='success'
                    disabled={loading}
                    onClick={loadBadge}>
                        Regenerate Badge
                    </Button>
                    <Button 
                    variant='outlined'
                    disabled={loading}
                    onClick={editAccount}>
                        {!loading ? 'Submit Edit' : 'Loading'}
                    </Button>
                    <Button
                    variant='contained'
                    onClick={() => {handleClose(); onClose()}}
                    disabled={loading}>
                        Close
                    </Button>
                </Stack>
            </Grid2>
            </>): 
            <Grid2>
              <div //Image Content
              style={scrollableContentStyle}>
                {badgeURLs?.front ? (
                  <> 
                    <img src={`${badgeURLs.front}`} //Change to production evniroment name for flask server eventually
                    />
                  </>
                ):(
                  <></>
                )}
                {badgeURLs?.back ? (
                  <>
                    <img 
                    src={`${badgeURLs.back}`}  //Change to production evniroment name for flask server eventually 
                    />
                  </>
                ):(
                  <></>
                )} 
              </div>
              <Stack 
                direction="row"
                display="flex" 
                alignItems="center" 
                justifyContent="center"
                spacing={4}
                sx={{mb:'.6rem'}}>
                <Button 
                variant='outlined'
                onClick={handlePrint}>
                    Print
                </Button>
                <Button
                variant='contained'
                onClick={handleBack}
                disabled={loading}>
                Back
                </Button>
                <Button
                variant='contained'
                color='error'
                onClick={() => {handleClose(); onClose()}}
                disabled={loading}>
                  Close
                </Button>
              </Stack>
            </Grid2>
            }
            </Dialog>
        </>
    )
}
