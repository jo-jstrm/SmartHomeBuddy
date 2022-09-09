import { useState } from "react";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { callClassifyDevices } from "../../rpc/clients/DeviceDatabaseClient";
import {styled} from "@mui/system";
import Typography from "@mui/material/Typography";


const StyledPaper = styled(Paper)(() => ({
  margin: 10,
  padding: 15
}));

const StyledDiv = styled('div')(() => ({
  display: "flex",
  justifyContent: "space-between",
  marginBottom: 5,
  alignItems: "center"
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
        <Button variant="outlined" size="medium" color="primary" onClick={classifyDevices}>
          Classify Devices
        </Button>
        <Typography>
          {classifierStatus}
        </Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
