import { useState } from "react";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import * as React from "react";
import { callHeartbeatService } from "../../rpc/clients/HeartbeatClient";
import { styled } from "@mui/system";
import Typography from "@mui/material/Typography";

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

export function Heartbeat() {
  const [identifierStatus, setIdentifierStatus] = useState(
    "Click the button to check the status of the Device Identifier."
  );
  const checkHeartbeat = () => {
    callHeartbeatService()
      .then(() => {
        setIdentifierStatus("Device Identifier is alive.");
      })
      .catch((err: Error) => {
        console.error("Catch: " + err.toString());
        setIdentifierStatus("No response from Device Identifier.");
      });
  };
  return (
    <React.Fragment>
      <StyledPaper>
        <StyledDiv>
          <Button
            variant="contained"
            size="medium"
            color="primary"
            onClick={checkHeartbeat}
          >
            Check Status of Device Identifier
          </Button>
          <Typography>{identifierStatus}</Typography>
        </StyledDiv>
      </StyledPaper>
    </React.Fragment>
  );
}
