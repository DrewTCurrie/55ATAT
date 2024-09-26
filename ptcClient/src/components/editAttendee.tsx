import * as React from 'react'
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import { useState } from 'react';
import { Button, Dialog, DialogTitle, Grid2, Stack } from '@mui/material';

interface badgeRespone {
    front: String,
    back?: String
  }

export default function EditAttendee(ID: string){
    //Handling the open and closing of edit modal
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
        //TODO, add data cleanup
        setOpen(false);
    }
    //Hook for handling going back from the print screen
    const handleBack = () => {
        setDisplayBadge(false);
    }

    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);

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
                    <img src="http://localhost:5000${badgeURLs?.front}" alt="Output 1" />
                </div>
                ${badgeURLs?.back ? (`
                <div class="page">
                    <img src=http://localhost:5000${badgeURLs.back} alt="Output 2" />
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
                    disabled={loading}>
                        {!loading ? 'Submit Edit' : 'Loading'}
                    </Button>
                    <Button
                    variant='contained'
                    onClick={handleClose}
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
                    <img src={`http://localhost:5000${badgeURLs.front}`} //Change to production evniroment name for flask server eventually
                    />
                  </>
                ):(
                  <></>
                )}
                {badgeURLs?.back ? (
                  <>
                    <img 
                    src={`http://localhost:5000${badgeURLs.back}`}  //Change to production evniroment name for flask server eventually 
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
                onClick={handleClose}
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