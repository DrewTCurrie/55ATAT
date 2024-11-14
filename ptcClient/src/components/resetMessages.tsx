import { Box, Button, Dialog, DialogContentText, DialogTitle, Stack, Typography } from "@mui/material";
import React from "react";
import { useState } from "react";


export default function ResetMessages(){
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

    const resetEverything = async () => {
        setLoading(true)
        try{
            const response = await fetch(`/api/resetEverything`)
            if (!response.ok) {
                throw new Error('Error deleting event' + response);
            }
            setDeleted(true)
        } catch(e) {
            console.error("Error deleting event", e);
        } finally {
            setLoading(false)
        }
    }

    return(
        <>
        <Button
            type="submit"
            variant="contained"
            color="error"
            fullWidth
            sx={{ my: '.4rem', backgroundColor: '#E59999' }}
            disabled={loading}
            onClick={handleClickOpen}
        >
            {loading ? 'Loading' : `Reset All Messages and Audio`}
        </Button>
        <Dialog
        open={open}
        onClose={handleClose}>
            <DialogTitle align='center'>Reset Everything</DialogTitle>
            <Box 
                    sx={{mb:'.6rem',mx:'.8rem'}}>
                    <DialogContentText
                    sx={{mb:'.6rem',mx:'.8rem'}}>
                    Warning: This resets every message and audio file in the system. Are you sure you want to do this?
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
                            Messages Successfully Reset.
                        </Typography>
                        :
                        <Button 
                            variant='contained'
                            onClick={resetEverything}
                            disabled={loading}
                            sx={{backgroundColor: '#6d9fb2' }}>
                            {!loading ? 'Delete' : 'Loading'}
                        </Button>}
                        <Button
                        variant='contained'
                        onClick={() =>{handleClose()}}
                        disabled={loading}
                        sx={{backgroundColor: '#e59999' }}>
                        Close
                        </Button>
                    </Stack>
            </Box>
        </Dialog>
        </>
    );
}