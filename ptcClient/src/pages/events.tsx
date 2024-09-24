import { Container, Box, Typography, Button, ButtonGroup} from '@mui/material';
import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { useState } from 'react'
import { ColDef } from 'ag-grid-community';
import ReportModal from '../components/reportModal';
import * as React from 'react';
import axios from 'axios';

//TODO: Make this table useable for Event Listings
interface IRow {
  make: string;
  model: string;
  price: number;
  electric: boolean;
}

function Events() {
    // Row Data: The data to be displayed.
    const [rowData, setRowData] = useState<IRow[]>([
      { make: "Tesla", model: "Model Y", price: 64950, electric: true },
      { make: "Ford", model: "F-Series", price: 33850, electric: false },
      { make: "Toyota", model: "Corolla", price: 29600, electric: false },
      { make: "Mercedes", model: "EQA", price: 48890, electric: true },
      { make: "Fiat", model: "500", price: 15774, electric: false },
      { make: "Nissan", model: "Juke", price: 20675, electric: false },
    ]);

    // Column Definitions: Defines the columns to be displayed.
    const [colDefs, setColDefs] = useState<ColDef<IRow>[]>([
      { field: "make" },
      { field: "model" },
      { field: "price" },
      { field: "electric" },
    ]);

    

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
        const response = await fetch(`http://192.168.1.12:5000/api/generateReport`, quickReport,).then(
          res => res.json()
        ).then(
           data => {
            axios.get(`http://192.168.1.12:5000/api/download/${data}`,{responseType: 'blob'}
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
        if(!response.ok){
          throw new Error(`Error: ${response.statusText}`);
        }
      } catch(e: any){
        console.log(e.message);
      }
    };


    return (
      <Container sx={{display: 'block', height: '100vh', width: '85vh'}}>
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
    };

export default Events
