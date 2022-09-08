import { useState } from "react";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { callClassifyDevices } from "../../rpc/clients/DeviceDatabaseClient";
import {styled} from "@mui/system";
import Typography from "@mui/material/Typography";


const StyledPaper = styled(Paper)(({ theme }) => ({
  margin: 15,
  padding: 20
}));

const StyledDiv = styled('div')(({theme}) => ({
  display: "flex",
  justifyContent: "space-between",
  marginBottom: 5,
}));

export default function Classification() {
  const [classifierStatus, setClassifierStatus] = useState(
    "Classify IoT devices based on the network data in your database."
  );
  const classifyDevices = () => {
    setClassifierStatus("Classifying. This might take a moment...");
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
    <StyledPaper>
      <StyledDiv>
        <Button variant="outlined" color="primary" onClick={classifyDevices}>
          Classify Devices
        </Button>
        <Typography align={"center"}>
          {classifierStatus}
        </Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
