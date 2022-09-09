import {useState} from "react";
import {queryAll} from "../../database/Database";
import {DbDevice} from "../../types/DeviceTypes";
import Title from "../common/Title";
import * as React from "react";
import {placeholder_db_device} from "../common/PlaceholderDevices";
import Paper from "@mui/material/Paper";
import {DataGrid, GridColDef} from "@mui/x-data-grid";
import {Button} from "@mui/material";
import { styled } from '@mui/system';

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 50 },
  { field: 'device_name', headerName: 'Device Name', width: 250 },
  { field: 'mac_address', headerName: 'MAC Address', width: 150 },
  { field: 'ip_address', headerName: 'IP Address', width: 150 },
];

const StyledPaper = styled(Paper)(() => ({
  margin: 10,
  padding: 10
}));

const StyledDiv = styled('div')(() => ({
  display: "flex",
  justifyContent: "space-between",
  marginBottom: 10,
}));

export default function DevicesGrid(): JSX.Element {
  const [devices, setDevices] = useState<DbDevice[]>(placeholder_db_device);
  const queryDevices = () => {
    const query = "SELECT * FROM devices";
    queryAll(query)
      .then((rows: DbDevice[]) => {
        console.log("Received devices.");
        setDevices(rows);
      })
      .catch((err: Error) => {
        console.log("Catch: " + err.toString());
        setDevices(placeholder_db_device);
      });
  };
  return (
    <React.Fragment>
      <StyledPaper>
        <StyledDiv>
          <Title> Devices </Title>
          <Button variant="outlined" size="small" color="primary" onClick={queryDevices}>
            Load Devices from Database
          </Button>
        </StyledDiv>
        <div style={{ height: 400, width: '100%' }}>
          <DataGrid rows={devices} columns={columns} pageSize={5} rowsPerPageOptions={[5]} checkboxSelection/>
        </div>
      </StyledPaper>
    </React.Fragment>
  );
}