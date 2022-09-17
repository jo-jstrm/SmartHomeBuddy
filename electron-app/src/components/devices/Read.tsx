import { useState } from "react";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { callClassifyDevices } from "../../rpc/clients/DeviceDatabaseClient";
import { styled } from "@mui/system";
import Typography from "@mui/material/Typography";

const { ipcRenderer } = window.require('electron');

const StyledPaper = styled(Paper)(() => ({
  margin: 10,
  padding: 15,
}));

const StyledDiv = styled("div")(() => ({
  display: "flex",
  justifyContent: "space-between",
  marginBottom: 5,
  alignItems: "center",
}));

export default function Read() {
  const [readStatus, setReadStatus] = useState(
    "Read network data from a capture file."
  );
  const classifyDevices = () => {
    setReadStatus("Reading capture file. This might take up to 15 minutes...");
    callClassifyDevices()
      .then(() => {
        setReadStatus("Succefully read all data!");
      })
      .catch((err: Error) => {
        console.error("Catch: " + err.toString());
        setReadStatus("No response from Device Identifier.");
      });
  };
  return (
    <StyledPaper>
      <StyledDiv>
        <Button
          variant="outlined"
          size="medium"
          color="primary"
          onClick={()=>{
            console.log("Button: using IPC.");
            ipcRenderer.send('getFilePath', 'some nice path')
          }}
        >
          Read Data from Capture File
        </Button>
        <Typography>{readStatus}</Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
