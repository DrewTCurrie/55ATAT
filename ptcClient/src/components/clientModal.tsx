import { Autocomplete, Box, Button, Dialog, DialogTitle, Grid2, Stack, TextField } from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import * as React from "react";

//Interface so modals know what to expect from the badgeURLs.
interface badgeRespone {
  front: String,
  back?: String
}

interface modalProps {
  onClose: () => void,
}

function ClientModal({onClose}: modalProps){
  //handling the opening and closing of the modal.
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
      //Clear all values in form
      setName('')
      setUsername('')
      setPwd('')
      setBadgeURLs(null)
      //Close modal
      setOpen(false);
      setDisplayBadge(false)
    };

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

    //Hook for displaying Badges after generation
    const [displayBadge, setDisplayBadge] = useState(false);
    const [badgeURLs, setBadgeURLs] =  useState<badgeRespone | null>();

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
    /*
     * Account Creation Handler, calls createAccount, then uses the ID to create an administrator and a badge
     */
    const createAccount = async () => {
      //Set Loading to True to disable button
      setLoading(true)
      //Create form data for accountData
      const accountData = new FormData();
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
      //Attempt to create an Account
      try {
        const response = await fetch(`/api/createAccount`, account)
        if (!response.ok) {
          throw new Error('Error creating account');
        }
        let userID = await response.text();
        userID = userID.trim().replace(/^"(.*)"$/, '$1');
        //If the user account is an administrator, attempt to create an administrator
        if(autoCompleteVal.roleAutoComplete.includes('Administrator')){
          const adminAccount = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
              "adminID": userID,
              "username": username,
              "password": pwd
            })
          }
          const adminResponse = await fetch(`/api/createAdmin`,adminAccount)
          if (!adminResponse.ok) {
            throw new Error('Error creating Administrator Account');
          }
        }
        //Attempt to generate a badge for the user.
        const badgeDetails = {
          method: 'POST',
          headers: {'Content-Type':'application/json',},
          body: JSON.stringify({
            "userID": userID
          })
        }
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
    };

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
    <Fragment>
        <Button onClick={handleClickOpen} >Create New Account </Button>
        <Dialog
            open={open}
            onClose={handleClose}>
            <DialogTitle align="center">Create New Account</DialogTitle>
            {!displayBadge ? //CHeck if displayBadge is ready, then display badge.
            <Grid2>
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
                    inputProps={{ maxLength: 256 }}
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
              <Stack 
                direction="row"
                display="flex" 
                alignItems="center" 
                justifyContent="center"
                spacing={4}
                sx={{mb:'.6rem'}}>
                <Button 
                  variant='outlined'
                  onClick={createAccount}
                  disabled={loading}>
                  {!loading ? 'Submit' : 'Loading'}
                </Button>
                <Button
                  variant='contained'
                  onClick={() => {handleClose(); onClose()}}
                  disabled={loading}>
                  Close
                </Button>
              </Stack>
            </Grid2> 
            : // BEGIN OTHER TERNARY
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
                  onClick={() => {handleClose(); onClose()}}
                  disabled={loading}>
                  Close
                </Button>
              </Stack>
            </Grid2>
            } 

        </Dialog>
    </Fragment>
    )
}
export default ClientModal
