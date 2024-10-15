import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import * as React from "react"; 
import { Box, TextField } from '@mui/material';
import { useCallback, useRef, useState } from 'react';
import { ColDef, GridApi, GridReadyEvent } from 'ag-grid-community';
// Row Data Interface
interface IRow {
    make: string;
    model: string;
    price: number;
    electric: boolean;
}
function Table(){
// Row Data: The data to be displayed.
const [rowData, setRowData] = useState<IRow[]>([
    { make: "Tesla", model: "Model Y", price: 64950, electric: true },
    { make: "Ford", model: "F-Series", price: 33850, electric: false },
    { make: "Toyota", model: "Corolla", price: 29600, electric: false },
    { make: "Mercedes", model: "EQA", price: 48890, electric: true },
    { make: "Fiat", model: "500", price: 15774, electric: false },
    { make: "Nissan", model: "Juke", price: 20675, electric: false },
  ]);

  // Column Definitions: Defines & controls grid columns.
  const [colDefs, setColDefs] = useState<ColDef[]>([
    { field: "make" },
    { field: "model" },
    { field: "price" },
    { field: "electric" },
  ]);

  //expose grid and column api for custom functionality
  const gridApiRef = useRef<GridApi | null>(null);

  const onGridReady = (params: GridReadyEvent) => {
    gridApiRef.current = params.api;
  };

     //Create a quick exterior filter for looking up table data
    // Function to apply quick filter using the exposed gridApi
    const onFilterTextBoxChanged = useCallback(() => {
        gridApiRef.current!.setGridOption(
          "quickFilterText",
          (document.getElementById("filter-text-box") as HTMLInputElement).value,
        );
      }, []);;

    return (
        <>
        <Box
              sx={{
                display: 'block',
                flexGrow: 1,
                bgcolor: 'background.paper',
              }}>
                <TextField
                type='text'
                id="filter-text-box"
                placeholder='Filter'
                onInput={onFilterTextBoxChanged}
                />
              <div
                className="ag-theme-quartz"
                style={{ height: 750, width: '125vh' }} // the Data Grid will fill the size of the parent container
              >
                <AgGridReact
                    rowData={rowData}
                    columnDefs={colDefs}
                    onGridReady={onGridReady}
              />
              </div>
        </Box>
        </>
    )
}

export default Table