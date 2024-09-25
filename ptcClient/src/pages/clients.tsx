import { Container, Box, Typography, Button, ButtonGroup} from '@mui/material';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useState, useEffect } from 'react'
import { ColDef, ICellRendererParams } from 'ag-grid-community';
import * as React from 'react';
import ClientModal from '../components/clientModal';
import EditAttendee from '../components/editAttendee';
import DeleteAttendee from '../components/deleteAttendee';

//This tells the table to know what datatypes to expect
interface IRow {
    ID: string;
    Initials: string;
    Roles: string | string[];
  }


function Clients() {
  // Column Definitions: Defines the columns to be displayed.
  const [colDefs, setColDefs] = useState<ColDef[]>([
  { field: "ID" },
  { field: "Initials" },
  { field: "Roles" },
  { field: "Edit",
    cellRenderer: (params: ICellRendererParams<IRow, number>) => {
      const ID = params.data?.ID ?? "";
      return EditAttendee(ID);
    } 
  },
  { field: "Delete",
    cellRenderer: (params: ICellRendererParams<IRow,number>) => {
      const ID = params.data?.ID ?? "";
      return DeleteAttendee(ID)
    }
  }
 ]);

 /* TABLE BUILDING
  Fetch all attendees in database (maybe limit this if db gets huge)
 */
const [rowData, setRowData] = useState<IRow[]>([])
const [hasFetchedRowData, setHasFetchedRoleData] = useState(false)
useEffect(()=> {
  if(!hasFetchedRowData){
    const fetchRoleData = async () => {
      try{
        const response = await fetch(`/api/getAllAttendees`)
        const data = await response.json();
        setRowData(data);
        setHasFetchedRoleData(true);
      } catch(e){
        console.error("Error fetching Attendees:", e);
      }
    };
    fetchRoleData(); //move to onload of table
  }
})

//Render Page
return (
<Container sx={{display: 'block', height: '100vh', width: '85vh'}}>
    <Box sx={{ display: 'flex', p: 1 }}>
      <Box sx={{ flex: 1}}/>
      <Box sx={{flex: 1, backgroundColor: 'gray', padding: 2 }}>
        <Typography variant="h6" color='white'>
          Clients
        </Typography>
      <ButtonGroup orientation="vertical" variant='contained'>
        <ClientModal/>
      </ButtonGroup>
      </Box>
    </Box>
    <Box
        sx={{
          display: 'block',
          flexGrow: 1,
          bgcolor: 'background.paper',
        }}>
        <div
          className="ag-theme-quartz"
          style={{ height: 500, width: '80vh' }} // the Data Grid will fill the size of the parent container
        >
          <AgGridReact
              rowData={rowData}
              columnDefs={colDefs}
        />
        </div>
        <Button variant='contained' sx={{display: 'flex'}}>New</Button>
    </Box>
  </Container>
  );
}

export default Clients