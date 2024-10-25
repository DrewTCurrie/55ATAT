import { AgGridReact } from 'ag-grid-react'; // React Data Grid Component
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";
import * as React from "react"; 
import { Box, TextField } from '@mui/material';
import { useCallback, useRef, useEffect, useState } from 'react';
import { ColDef, GridApi, GridReadyEvent } from 'ag-grid-community'


//Table Interface
interface AgGridWrapperProps<T> {
  rowData: T[];                 
  colDefs: ColDef<any, any>[];
}

const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);

    // Clean up the event listener on component unmount
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};


const Table = <T extends unknown>({ rowData, colDefs }: AgGridWrapperProps<T>) => {

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

    //Get Window Height, adjust values.
    const {width, height} = useWindowSize();
    const tableWidth = width * .80;
    const tableHeight = height *.65;

    return (
      <>
        <Box
        sx={{
          color: 'black'
        }}>
          <Box
            sx={{
              display:'flex',
              justifyContent: 'flex-start'
            }}>
            <TextField
                    type='text'
                    id="filter-text-box"
                    placeholder='Search...'
                    onInput={onFilterTextBoxChanged}
                    sx={{mb: '.2rem'}}
                    size='small'
                    />
          </Box>
          <Box
                sx={{
                  display: 'flex',
                  flexGrow: 1,
                  bgcolor: 'background.paper',
                  alignContent: 'center'
                }}> 
                <div
                  className="ag-theme-material"
                  style={{ height: tableHeight, width: tableWidth }} // the Data Grid will fill the size of the parent container
                >
                  <AgGridReact
                      rowData={rowData}
                      columnDefs={colDefs}
                      onGridReady={onGridReady}
                      enableCellTextSelection
                />
                </div>
          </Box>
        </Box>
      </>
    )
}

export default Table