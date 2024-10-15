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

//This function is used to set the size of the table to take as much room as possible, and adjust with window size
const onGridSizeChanged = useCallback(
  (params: GridSizeChangedEvent) => {
    // get the current grids width
    var gridWidth = document.querySelector(".ag-body-viewport")!.clientWidth;
    // keep track of which columns to hide/show
    var columnsToShow = [];
    var columnsToHide = [];
    // iterate over all columns (visible or not) and work out
    // now many columns can fit (based on their minWidth)
    var totalColsWidth = 0;
    var allColumns = params.api.getColumns();
    if (allColumns && allColumns.length > 0) {
      for (var i = 0; i < allColumns.length; i++) {
        var column = allColumns[i];
        totalColsWidth += column.getMinWidth();
        if (totalColsWidth > gridWidth) {
          columnsToHide.push(column.getColId());
        } else {
          columnsToShow.push(column.getColId());
        }
      }
    }
    // show/hide columns based on current grid width
    params.api.setColumnsVisible(columnsToShow, true);
    params.api.setColumnsVisible(columnsToHide, false);
    // wait until columns stopped moving and fill out
    // any available space to ensure there are no gaps
    window.setTimeout(() => {
      params.api.sizeColumnsToFit();
    }, 10);
  },
  [window],
);

//When a modal closes, reload the table.
const handleModalClose = useCallback(() => {
  fetchRowData();
},[]);

//Render Page
return (
<Container sx={{ display: 'flex', flexDirection: 'column', height: '100vh', minWidth: '100%' }}>
    <Box sx={{ display: 'flex', p: 1 }}>
      <Box sx={{ flex: 1}}/>
      <Box sx={{flex: 1, backgroundColor: 'gray', padding: 2 }}>
        <Typography variant="h6" color='white'>
          Clients
        </Typography>
      <ButtonGroup orientation="vertical" variant='contained'>
        <ClientModal onClose={handleModalClose}/>
      </ButtonGroup>
      </Box>
    </Box>
    <Box
        sx={{
          flexGrow: 1,         
          display: 'flex',     
          flexDirection: 'column',
          bgcolor: 'background.paper',
        }}>
        <div
          className="ag-theme-quartz"
          //TODO: Make webpage take as much screenspace as possible for ease of viewing
          style={{ height: 750, width: '125vh' }} // the Data Grid will fill the size of the parent container
        >
          <AgGridReact
              rowData={rowData}
              columnDefs={colDefs}
              onGridSizeChanged={onGridSizeChanged}
        />
        </div>
    </Box>
  </Container>
  );
}

export default Clients