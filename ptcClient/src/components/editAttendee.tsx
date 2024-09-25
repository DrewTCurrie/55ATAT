import * as React from 'react'
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import { useState } from 'react';
import { Dialog, DialogTitle } from '@mui/material';

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
                {ID}
            </Dialog>
        </>
    )
}