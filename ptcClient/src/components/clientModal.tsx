import { Button, Dialog, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import * as React from "react";

//Wayne's QR code generator will likely go here.
function ClientModal(){
    const [open, setOpen] = useState(false);

    const handleClickOpen = () => {
      setOpen(true);
    };
    //Make submit condition
    const handleClose = () => {
      setOpen(false);
    };

    return(
    <Fragment>
        <Button onClick={handleClickOpen} >Create New Account </Button>
        <Dialog
            open={open}
            onClose={handleClose}>
            <DialogTitle>Create New Account</DialogTitle>
        </Dialog>
    </Fragment>
    )
}
export default ClientModal
