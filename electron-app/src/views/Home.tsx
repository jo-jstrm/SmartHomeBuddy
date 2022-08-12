import * as React from "react";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Chart from "../components/home/Chart";
import Deposits from "../components/home/Deposits";
import Orders from "../components/home/Orders";
import Copyright from "../components/common/Copyright";
import { Heartbeat } from "../components/home/Heartbeat";

export default function Home() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Heartbeat />
        {/* Chart */}
        {/*<Grid item xs={12} md={8} lg={9}>*/}
        {/*  <Paper*/}
        {/*    sx={{*/}
        {/*      p: 2,*/}
        {/*      display: "flex",*/}
        {/*      flexDirection: "column",*/}
        {/*      height: 240,*/}
        {/*    }}*/}
        {/*  >*/}
        {/*    <Chart />*/}
        {/*  </Paper>*/}
        {/*</Grid>*/}
        {/*/!* Recent Deposits *!/*/}
        {/*<Grid item xs={12} md={4} lg={3}>*/}
        {/*  <Paper*/}
        {/*    sx={{*/}
        {/*      p: 2,*/}
        {/*      display: "flex",*/}
        {/*      flexDirection: "column",*/}
        {/*      height: 240,*/}
        {/*    }}*/}
        {/*  >*/}
        {/*    <Deposits />*/}
        {/*  </Paper>*/}
        {/*</Grid>*/}
        {/*/!* Recent Orders *!/*/}
        {/*<Grid item xs={12}>*/}
        {/*  <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>*/}
        {/*    <Orders />*/}
        {/*  </Paper>*/}
        {/*</Grid>*/}
      </Grid>
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}