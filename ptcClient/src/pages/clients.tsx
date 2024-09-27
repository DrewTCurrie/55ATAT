import { Container, Box, Typography, Button, ButtonGroup} from '@mui/material';
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
  const [colDefs, setColDefs] = useState<ColDef[]>([
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
      return EditAttendee(ID,Initials,Roles);
    } 
  },
  { field: "Delete",
    flex: 1,
    cellRenderer: (params: ICellRendererParams<IRow,number>) => {
      const ID = params.data?.ID ?? "";
      const Initials = params.data?.Initials ?? "";
      return DeleteAttendee(ID,Initials)
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

//Render Page
return (
<Container sx={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100%' }}>
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
          flexGrow: 1,         
          display: 'flex',     
          flexDirection: 'column',
          bgcolor: 'background.paper',
        }}>
        <div
          className="ag-theme-quartz"
          style={{ height: 500, width: '80vh' }} // the Data Grid will fill the size of the parent container
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