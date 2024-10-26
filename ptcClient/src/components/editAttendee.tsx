import * as React from 'react'
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import { useEffect, useState } from 'react';
import { Autocomplete, Box, Button, Dialog, DialogTitle, Grid2, Slider, Stack, TextField, Typography } from '@mui/material';
import Cropper, { Area, Point } from 'react-easy-crop';
import { getCroppedImg } from '../functions/cropUtils';
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

function readFile(file: File): Promise<string> {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.addEventListener('load', () => resolve(reader.result as string), false)
    reader.readAsDataURL(file)
  })
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
      setImageSrc('')
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
    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if(file){
        const fileType = file.type;
        if(fileType.startsWith('image/')){
          console.log(file);
          let imageDataUrl = await readFile(file)
          setImageSrc(imageDataUrl)
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
    /**
     *  Image Cropping Handler
     * 
     */
        const [imageSrc, setImageSrc] = useState<string>('')
        const [crop, setCrop] = useState<Point>({ x: 0, y: 0 });
        const [zoom, setZoom] = useState(1);
        const [rotation, setRotation] = useState(0)
        const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);
        const [croppedImage, setCroppedImage] = useState<File | null>()
        const handleCropComplete = (_croppedArea: Area, croppedAreaPixels: Area) => {
          setCroppedAreaPixels(croppedAreaPixels);
        };
    
        /**
         * This handles creating the adjusted image for submission
         */
        const showCroppedImage = async () => {
          try {
            const croppedImage = await getCroppedImg(
              imageSrc,
              croppedAreaPixels,
              rotation
            )
            console.log('donee', { croppedImage })
            setCroppedImage(croppedImage)
            console.log(croppedImage)
            return croppedImage
    
          } catch (e) {
            console.error(e)
            return null
          }
        }

    /*
    * Account Editing Handler, calls editAccount, then uses the ID to edit an administrator if either is updated
    */
    const editAccount = async () => {
      //Set Loading to True to disable button
      setLoading(true)
      try{
        //Get Cropped Image
        const croppedImage = await showCroppedImage(); 
        //Create form data for accountData
        const accountData = new FormData();
        accountData.append('id',ID);
        accountData.append('name',name);
        accountData.append('roles',JSON.stringify(autoCompleteVal.roleAutoComplete))
        //Check if a file exists, if true append.
        if(croppedImage){
          accountData.append('file', croppedImage)
        }
        const account = {
          method: 'POST',
          body: accountData
        }
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
    const scrollableContentStyle = {
      display: 'flex', // Use flexbox to align items
      justifyContent: 'center', // Center images horizontally
      alignItems: 'center', // Align images vertically
      overflow: 'hidden', // Prevent scrolling
    };

    const imageStyle = {
      maxWidth: '50%', // Each image takes up half the width of the container
      height: 'auto', // Maintain aspect ratio
      margin: '0 10px', // Optional: add space between images
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
                    {imageSrc && <>
                      <Box
                        sx={{
                          position: "relative",
                          width: "100%",
                          height: 300,
                          background: "#333",
                        }}
                      >
                        <Cropper
                          image={imageSrc}
                          crop={crop}
                          zoom={zoom}
                          rotation={rotation}
                          aspect={1}
                          cropShape="round"
                          restrictPosition={false}
                          onCropChange={setCrop}
                          onZoomChange={setZoom}
                          onCropComplete={handleCropComplete}
                          onRotationChange={setRotation}
                        />
                      </Box>
                      <Box>
                        <Box>
                          <Typography
                            variant="overline"
                          >
                            Zoom
                          </Typography>
                          <Slider
                            value={zoom}
                            min={1}
                            max={3}
                            step={0.1}
                            aria-labelledby="Zoom"
                            onChange={(_e, zoom) => setZoom(zoom as number)}
                          />
                        </Box>
                        <Box>
                          <Typography
                            variant="overline"
                          >
                            Rotation
                          </Typography>
                          <Slider
                            value={rotation}
                            min={0}
                            max={360}
                            step={1}
                            aria-labelledby="Rotation"
                            onChange={(_e, rotation) => setRotation(rotation as number)}
                          />
                      </Box>
                      </Box>
                    </>}
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
              <Box //Image Content
              style={scrollableContentStyle}>
                {badgeURLs?.front ? (
                  <> 
                    <img src={`${badgeURLs.front}?${new Date().getTime()}`} style={imageStyle}
                    />
                  </>
                ):(
                  <></>
                )}
                {badgeURLs?.back ? (
                  <>
                    <img 
                    src={`${badgeURLs.back}?${new Date().getTime()}`} style={imageStyle}
                    />
                  </>
                ):(
                  <></>
                )} 
              </Box>
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
