import {useEffect, useState} from "react";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { styled } from "@mui/system";
import Typography from "@mui/material/Typography";
import {callRead} from "../../rpc/clients/ReadClient";

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
  useEffect( () => {
    ipcRenderer.on('captureFilePath', (event, filePaths) => {
      console.log("ipc renderer.")
      // Display capture file path.
      setReadStatus("Reading file at path: " + filePaths[0] + ". This might take up to 15 minutes...");
      // Call read via RPC.
      callRead(filePaths[0])
        .then(() => {
          setReadStatus("Succefully read all data!");
        })
        .catch((err: Error) => {
          console.error("Catch: " + err.toString());
          setReadStatus("No response from Device Identifier.");
        });
    });
  });
  return (
    <StyledPaper>
      <StyledDiv>
        <Button
          variant="outlined"
          size="medium"
          color="primary"
          onClick={()=>{
            console.log("Button: using IPC.");
            ipcRenderer.send('getCaptureFilePath');
          }}
        >
          Read Data from Capture File
        </Button>
        <Typography>{readStatus}</Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
