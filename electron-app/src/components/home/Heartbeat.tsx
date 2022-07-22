import {useState} from "react";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import {Button} from "@mui/material";
import * as React from "react";
import {callHeartbeatServer} from "../../rpc/HeartbeatClient"

export function Heartbeat() {
    const [identifierStatus, setIdentifierStatus] = useState("Click the button to check the status of the Device Identifier.")
    const checkHeartbeat = () => {
        callHeartbeatServer()
            .then((response) => {
                setIdentifierStatus("Device Identifier is alive: " + response.getAlive().toString())
            })
            .catch(() => {
                setIdentifierStatus("No response from Device Identifier.")
        });
    }
    return (
        <React.Fragment>
            <Grid item xs={12}>
                <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
                    <Button variant="contained" color="primary" onClick={checkHeartbeat}>
                        Check Status of Device Identifier
                    </Button>
                </Paper>
            </Grid>
            <Grid item xs={12}>
                <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
                    {/*Trigger page reload*/}
                    {identifierStatus}
                </Paper>
            </Grid>
        </React.Fragment>
    );
}