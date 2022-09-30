import { useEffect, useState } from "react";
import * as React from "react";
import { FileOpen } from "@mui/icons-material";
import CloseIcon from "@mui/icons-material/Close";
import { Alert, Box, Button, Collapse, InputAdornment } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/system";
import { callRead } from "../../rpc/clients/ReadClient";

const { ipcRenderer } = window.require("electron");

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
  const [measurement, setMeasurement] = useState("main");
  const [successOpen, setSuccessOpen] = React.useState(false);
  const [failureOpen, setFailureOpen] = React.useState(false);
  useEffect(() => {
    ipcRenderer.on("captureFilePath", (event, filePaths) => {
      console.log("IPC: 'captureFilePath'");
      setPath(filePaths[0]);
    });
  });
  return (
    <StyledPaper>
      <Box sx={{ width: "100%" }}>
        <Collapse in={successOpen}>
          <Alert
            severity="success"
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setSuccessOpen(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ mb: 2 }}
          >
            Successfully read all data!
          </Alert>
        </Collapse>
        <Collapse in={failureOpen}>
          <Alert
            severity="error"
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setFailureOpen(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ mb: 2 }}
          >
            Failed to read data.
          </Alert>
        </Collapse>
      </Box>
      <Box
        component="form"
        sx={{ p: "2px 4px", display: "flex", alignItems: "center" }}
      >
        <Button
          sx={{ p: "10px" }}
          aria-label="submit"
          variant="contained"
          onClick={() => {
            console.log("Button: using IPC.");
            // Call read via RPC.
            callRead(path, measurement)
              .then(() => {
                setSuccessOpen(true);
              })
              .catch((err: Error) => {
                console.error("Catch: " + err.toString());
                setFailureOpen(true);
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
            endAdornment: (
              <InputAdornment position="start">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={() => {
                    console.log("Button: using IPC.");
                    ipcRenderer.send("getCaptureFilePath");
                  }}
                  edge="end"
                >
                  <FileOpen />
                </IconButton>
              </InputAdornment>
            ),
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
    </StyledPaper>
  );
}
