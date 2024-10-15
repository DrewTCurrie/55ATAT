import { Container, Box, Typography, Button, ButtonGroup} from '@mui/material';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useCallback, useEffect, useState } from 'react'
import { ColDef, ICellRendererParams } from 'ag-grid-community';
import ReportModal from '../components/reportModal';
import * as React from 'react';
import axios from 'axios';
import NewEvent from '../components/newEventModal';
import DeleteEvent from '../components/deleteEvent';
import EditEvent from '../components/editEvent';


interface IRow {
  EventID: string,
  ID: string,
  Initials: string,
  Timestamp: string,
  Absent: boolean,
  TIL_Violation: boolean,
  AdminInitials: string,
  Comment: string
}

function Events() {
    // Column Definitions: Defines the columns to be displayed.
    const [colDefs] = useState<ColDef[]>([
      { field: "EventID",
        hide: true
       },
      { field: "ID",
        hide: true
       },
      { field: "Initials",
        flex: 1
       },
      { field: "Timestamp",
        flex: 4,
        // cellRenderer: (params: ICellRendererParams<IRow,number>) => {
        //   const date = new Date(params.data?.Timestamp ?? "")
        //   return date;
        // }
       },
      { field: "Absent",
        flex: 1,
        cellRenderer: (params: ICellRendererParams<IRow, number>) => {
          if (params.data?.Absent === false) {
            return <Typography sx={{my:'.3rem'}}>No</Typography>;
          } else {
            return <Typography color='red' sx={{my:'.3rem'}}>Yes</Typography>;
          }
        }
      },
      { field: "TIL_Violation",
        headerName: 'TIL',
        flex: 1,
        cellRenderer: (params: ICellRendererParams<IRow, number>) => {
          if (params.data?.TIL_Violation === false) {
            return <Typography sx={{my:'.3rem'}}>No</Typography>;
          } else {
            return <Typography color='red' sx={{my:'.3rem'}}>Yes</Typography>;
          }
        }
      },
      { field: "Edit",
        headerName: 'Edit',
        flex: 1,
        cellRenderer: (params: ICellRendererParams<IRow, number>) => {
          const EventID = params.data?.EventID ?? ""; 
          const Initials = params.data?.Initials ?? "";
          const Timestamp = params.data?.Timestamp ?? "";
          const Absent = params.data?.Absent ?? false
          const TIL = params.data?.TIL_Violation ?? false
          const AdminInitials = params.data?.AdminInitials ?? "";
          const Comment = params.data?.Comment ?? "";
          return <EditEvent onClose={handleModalClose} EventID={EventID} Initials={Initials} Timestamp={Timestamp} Absent={Absent} TIL={TIL} AdminInitials={AdminInitials} Comment={Comment}/>
        } 
      },
      { field: "Delete",
        flex: 1,
        cellRenderer: (params: ICellRendererParams<IRow,number>) => {
          const EventID = params.data?.EventID ?? "";
          const Initials = params.data?.Initials ?? "";
          const Timestamp = new Date(params.data?.Timestamp ?? "")
          return <DeleteEvent onClose={handleModalClose} ID={EventID} Initials={Initials} Timestamp={Timestamp.toLocaleString()}/>
        }
      },
      { field: "AdminInitials",
        hide: true
      },
      { field: "Comment",
        hide: true
      }
    ]);

    /* TABLE BUILDING
    Fetch all attendees in database (maybe limit this if db gets huge)
    */
    const [rowData, setRowData] = useState<IRow[]>([])
    const [hasFetchedRowData, setHasFetchedRowData] = useState(false)
    const fetchRowData = async () => {
      try{
        const response = await fetch(`/api/getRecentEvents`)
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

    const generateQuickReport = async () => {
      //JSON for a quick report, (7 days back), Python will autofill information.
      const quickReport = { 
          method: 'POST',
          headers: {'Content-Type': 'application/json',},
          body: JSON.stringify({
            "name": null,
            "role": null,
            "startDate": null,
            "endDate": null})}
      //Try 
      console.log(quickReport)
      try {
        const response = await fetch(`/api/generateReport`, quickReport,).then(
          res => res.json()
        ).then(
           data => {
            axios.get(`/api/download/${data}`,{responseType: 'blob'}
            ).then((downloadRes) => {
              const url = window.URL.createObjectURL(new Blob([downloadRes.data]));
              const link = document.createElement('a');
              link.href=url;
              link.setAttribute('download',`${data}`);
              document.body.appendChild(link);
              link.click();
            })
          }
        );
      } catch(e: any){
        console.log(e.message);
      }
    };

    //When a modal closes, reload the table.
    const handleModalClose = useCallback(() => {
      fetchRowData();
    },[]);
    
    return (
      <Container sx={{display: 'block', height: '100vh', width: '175vh'}}>
          <Box sx={{ display: 'flex', p: 1 }}>
            <Box sx={{ flex: 1}}/>
            <Box sx={{flex: 1, backgroundColor: 'gray', padding: 2 }}>
              <Typography variant="h6" color='white'>
                Reports
              </Typography>
            <ButtonGroup orientation="vertical" variant='contained'>
              <Button sx={{marginBottom:.5}} onClick={generateQuickReport}>Generate Quick Report (1 Week)</Button>
              <ReportModal/>
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
                style={{ height: 750, width: '125vh' }} // the Data Grid will fill the size of the parent container
              >
                <AgGridReact
                    rowData={rowData}
                    columnDefs={colDefs}
              />
              </div>
              <NewEvent onClose={handleModalClose}></NewEvent>
          </Box>
        </Container>
      );
    };

export default Events
