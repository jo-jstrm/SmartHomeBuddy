import {useEffect, useState} from "react";
import Paper from "@mui/material/Paper";
import {Box, Button, InputAdornment} from "@mui/material";
import * as React from "react";
import { styled } from "@mui/system";
import Typography from "@mui/material/Typography";
import {callRead} from "../../rpc/clients/ReadClient";
import IconButton from "@mui/material/IconButton";
import {FileOpen} from "@mui/icons-material";
import TextField from '@mui/material/TextField';

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

export function Read() {
  const [readStatus, setReadStatus] = useState("");
  const [path, setPath] = useState("");
  const [measurement, setMeasurement] = useState("");
  useEffect( () => {
    ipcRenderer.on('captureFilePath', (event, filePaths) => {
      console.log("IPC: 'captureFilePath'")
      setPath(filePaths[0]);
    });
  });
  return (
    <StyledPaper>
      <Box
        component="form"
        sx={{ p: '2px 4px', display: 'flex', alignItems: 'center'}}
      >
        <Button sx={{p: '10px'}}
                aria-label="submit"
                variant="contained"
                onClick={()=>{
                  console.log("Button: using IPC.");
                  // Call read via RPC.
                  callRead(path, measurement)
                    .then(() => {
                      setReadStatus("Succefully read all data!");
                    })
                    .catch((err: Error) => {
                      console.error("Catch: " + err.toString());
                      setReadStatus("No response from Device Identifier.");
                    });
                }}
        >
          Read
        </Button>
        <TextField
          label="Path"
          id="capture-path-input-field"
          variant="filled"
          required
          sx={{ ml: 1, flex: 1 }}
          value={path}
          placeholder="Enter path to capture file"
          onChange={(event) => {
            setPath(event.target.value);
          }}
          InputProps={{
            endAdornment: <InputAdornment position="start"><IconButton
              aria-label="toggle password visibility"
              onClick={() => {
                console.log("Button: using IPC.");
                ipcRenderer.send('getCaptureFilePath');
              }}
              edge="end"
            >
              <FileOpen/>
            </IconButton></InputAdornment>,
          }}
        />
        <TextField
          label="Measurement"
          id="measurement-input-field"
          variant="filled"
          sx={{ ml: 1, flex: 1 }}
          value={measurement}
          placeholder="Default: main"
          onChange={(event) => {
            setMeasurement(event.target.value);
          }}
        />
      </Box>
    <StyledDiv>
      <Typography>{readStatus}</Typography>
    </StyledDiv>
    </StyledPaper>

  );
}