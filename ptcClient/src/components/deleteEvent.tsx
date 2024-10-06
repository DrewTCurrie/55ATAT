import * as React from 'react'
import IconButton from '@mui/material/IconButton';
import { useState } from 'react';
import { Box, Button, Dialog, DialogContentText, DialogTitle, Stack, Typography } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

interface modalProps {
    onClose: () => void,
    ID: string,
    Initials: string,
    Timestamp: string
  }

export default function DeleteEvent({onClose,ID,Initials,Timestamp}: modalProps){
    //Handling the open and closing of edit modal
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    }

    //Hook for handling the modal loading (waiting for input)
    const [loading, setLoading] = useState(false);
    const [deleted, setDeleted] = useState(false);

    //This const calls /api/delete account from the api, and deletes an account.
    const deleteAccount = async () => {
        setLoading(true)
        const deleteJSON = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                "ID": ID
            })
        }
        try{
            const response = await fetch(`/api/deleteEvent`, deleteJSON)
            if (!response.ok) {
                throw new Error('Error deleting event' + response);
            }
            setLoading(false)
            setDeleted(true)
        } catch(e) {
            console.error("Error deleting event", e);
            setLoading(false)
        }
    }
    return(
        <>
            <IconButton 
                onClick={handleClickOpen}
                aria-label='delete'>
                <DeleteIcon/>
            </IconButton>
            <Dialog
            open={open}
            onClose={handleClose}>
                <DialogTitle align='center'>Delete Account</DialogTitle>
                <Box 
                    sx={{mb:'.6rem',mx:'.8rem'}}>
                    <DialogContentText
                    sx={{mb:'.6rem',mx:'.8rem'}}>
                    Are you sure you want to delete event {ID}?
                    </DialogContentText>
                    <DialogContentText
                    sx={{mb:'.6rem',mx:'.8rem', mt: '.5rem' }}>
                    Account:{Initials}: Timestamp:{Timestamp}
                    </DialogContentText>
                    <Stack                
                        direction="row"
                        display="flex" 
                        alignItems="center" 
                        justifyContent="center"
                        spacing={4}
                        sx={{mb:'.6rem'}}>
                        {deleted ? 
                        <Typography variant="h6" color='green'>
                            Account Successfully Deleted
                        </Typography>
                        :
                        <Button 
                            variant='outlined'
                            onClick={deleteAccount}
                            disabled={loading}>
                            {!loading ? 'Delete' : 'Loading'}
                        </Button>}
                        <Button
                        variant='contained'
                        onClick={() =>{handleClose(); onClose()}}
                        disabled={loading}>
                        Close
                        </Button>
                    </Stack>
                </Box>
            </Dialog>
        </>
    )
}