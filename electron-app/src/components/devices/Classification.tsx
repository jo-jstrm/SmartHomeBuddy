import { useState } from "react";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { callClassifyDevices } from "../../rpc/clients/DeviceDatabaseClient";

export default function Classification() {
  const [classifierStatus, setClassifierStatus] = useState(
    "Classify IoT devices based on the network data in your database."
  );
  const classifyDevices = () => {
    setClassifierStatus("Classifying. This might take a moment...")
    callClassifyDevices()
      .then(() => {
        setClassifierStatus("Classified!");
      })
      .catch((err: Error) => {
        console.error("Catch: " + err.toString());
        setClassifierStatus("No response from Device Identifier.");
      });
  };
  return (
    <Grid container spacing={1}>
      <Grid item xs={12}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          <Button variant="contained" color="primary" onClick={classifyDevices}>
            Classify Devices
          </Button>
        </Paper>
      </Grid>
      <Grid item xs={12}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          {/*Trigger page reload*/}
          {classifierStatus}
        </Paper>
      </Grid>
    </Grid>
  );
}