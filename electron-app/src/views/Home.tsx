import * as React from "react";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Copyright from "../components/common/Copyright";
import DetectedDevices from "../components/home/DetectedDevices";
import { Typography } from "@mui/material";

export default function Home() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container sx={{ my: 10 }}>
        <Typography
          sx={{
            fontSize: "48px",
            width: "100%",
            fontFamily: "Quicksand",
            // display: 'inline',
            mx: 0.5,
          }}
          align="center"
        >
          Welcome to SmartHomeBuddy!
        </Typography>
      </Grid>
      <DetectedDevices sx={{ mt: 2, mb: 2 }} />
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
