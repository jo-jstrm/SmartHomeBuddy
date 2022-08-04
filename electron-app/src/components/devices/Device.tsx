import * as React from "react";
import Typography from "@mui/material/Typography";
import { Grid } from "@mui/material";

export default function Device(props: {
  name: string;
  icon: any;
  status: string;
  index: number;
  mac: string;
  action: any;
}) {
  return (
    <React.Fragment>
      <Grid item xs={1} justifyContent="left">
        {props.icon}
      </Grid>
      <Grid
        item
        xs={10}
        container
        direction="column"
        justifyContent="flex-start"
        spacing={1}
      >
        <Grid
          item
          xs
          container
          justifyContent="flex-start"
          alignItems="center"
          spacing={1}
        >
          <Grid item>
            <Typography variant="subtitle1">{props.name}</Typography>
          </Grid>
          <Grid item>
            <Typography variant="body2" color="text.secondary">
              {props.mac}
            </Typography>
          </Grid>
        </Grid>
        <Grid item xs container direction="row" spacing={1}>
          <Grid item xs>
            <Typography gutterBottom variant="body1">
              {props.status}
            </Typography>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={1} justifyContent="right">
        {props.action}
      </Grid>
    </React.Fragment>
  );
}
