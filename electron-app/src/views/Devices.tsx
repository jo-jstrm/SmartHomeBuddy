import * as React from "react";
import Container from "@mui/material/Container";
import Classification from "../components/devices/Classification";
import Copyright from "../components/common/Copyright";
import DeviceList from "../components/devices/DeviceList";


export default function Devices() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Classification />
      <DeviceList sx={{mt: 2, mb: 2}} />
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
