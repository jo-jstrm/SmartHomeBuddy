import * as React from "react";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import { Grid } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import RefreshIcon from "@mui/icons-material/Refresh";

export const DeviceContent = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  color: theme.palette.text.secondary,
  elevation: 2,
}));

export default function Device(props: {
  name: string;
  icon: any;
  status: string;
  index: number;
}) {
  return (
    <DeviceContent key={props.index}>
      <Grid container spacing={1} alignItems="center">
        <Grid item key="icon" xs={1}>
          {props.icon}
        </Grid>
        <Grid item key="device-name" xs={6}>
          <Typography variant="h5">{props.name}</Typography>
        </Grid>
        <Grid item key="device-ip-adress" xs={2}>
          <Typography variant="body1">IP address</Typography>
        </Grid>
        <Grid item key="device-status" xs={2}>
          <Typography variant="body1">{props.status}</Typography>
        </Grid>
        <Grid item key="refresh-button" xs={1}>
          <IconButton aria-label="refresh button" size="medium">
            <RefreshIcon />
          </IconButton>
        </Grid>
      </Grid>
    </DeviceContent>
  );
}
