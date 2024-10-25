import { Container, Box, Typography, ButtonGroup} from '@mui/material';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useState, useEffect, useCallback } from 'react'
import { ColDef, GridSizeChangedEvent, ICellRendererParams } from 'ag-grid-community';
import * as React from 'react';
import ClientModal from '../components/clientModal';
import EditAttendee from '../components/editAttendee';
import DeleteAttendee from '../components/deleteAttendee';
import Table from '../components/table';

//This tells the table to know what datatypes to expect
interface IRow {
    ID: string;
    Initials: string;
    Roles: string | string[];
  }

function Clients() {
  // Column Definitions: Defines the columns to be displayed.
  const [colDefs] = useState<ColDef[]>([
  { field: "ID" },
  { field: "Initials" },
  { field: "Roles" },
  { field: "Edit",
    headerName: 'Edit',
    flex: 1,
    cellRenderer: (params: ICellRendererParams<IRow, number>) => {
      const ID = params.data?.ID ?? "";
      const Initials = params.data?.Initials ?? "";
      const Roles = params.data?.Roles ?? "";
      return <EditAttendee onClose={handleModalClose} ID={ID} Initials={Initials} Roles={Roles}/>
    } 
  },
  { field: "Delete",
    flex: 1,
    cellRenderer: (params: ICellRendererParams<IRow,number>) => {
      const ID = params.data?.ID ?? "";
      const Initials = params.data?.Initials ?? "";
      return <DeleteAttendee onClose={handleModalClose} ID={ID} Initials={Initials}/>
    }
  }
 ]);

 /* TABLE BUILDING
  Fetch all attendees in database (maybe limit this if db gets huge)
 */
const [rowData, setRowData] = useState<IRow[]>([])
const [hasFetchedRowData, setHasFetchedRowData] = useState(false)
const fetchRowData = async () => {
  try{
    const response = await fetch(`/api/getAllAttendees`)
    const data = await response.json();
    setRowData(data);
    setHasFetchedRowData(true);
  } catch(e){
    console.error("Error fetching Attendees:", e);
  }
}

//This use effect loads Row data on webpage load
useEffect(()=> {
  if(!hasFetchedRowData){
      fetchRowData();
    };
  }
)

//When a modal closes, reload the table.
const handleModalClose = useCallback(() => {
  fetchRowData();
},[]);

//Render Page
return (
<Container>
    <Box sx={{ display: 'flex', p: '5px' }}>
      <Box sx={{ flex: 1}}/>
      <Box sx={{ flex: 1, backgroundColor: 'gray', padding: '2px', mx: '.4rem' }}>
        <Typography variant="h6" color='white'>
          Attendees
        </Typography>
      <ButtonGroup orientation="vertical" variant='contained'>
        <ClientModal onClose={handleModalClose}/>
      </ButtonGroup>
      </Box>
    </Box>
    <Table rowData={rowData} colDefs={colDefs}/>
  </Container>
  );
}

export default Clients