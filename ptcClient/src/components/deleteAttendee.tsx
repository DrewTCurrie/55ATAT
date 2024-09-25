import * as React from 'react'
import IconButton from '@mui/material/IconButton';
import { useState } from 'react';
import { Box, Dialog, DialogContentText, DialogTitle } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';


export default function DeleteAttendee(ID: string){
    //Handling the open and closing of edit modal
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
      setOpen(true);
    };
    const handleClose = () => {
        //TODO, add data cleanup
        setOpen(false);
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
                <Box sx={{mb:'.6rem',mx:'.8rem'}}>
                    <DialogContentText
                    sx={{mb:'.6rem',mx:'.8rem'}}>
                    Are you sure you want to delete account {ID}?</DialogContentText>
                </Box>
            </Dialog>
        </>
    )
}