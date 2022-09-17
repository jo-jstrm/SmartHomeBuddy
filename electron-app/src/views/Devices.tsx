import * as React from "react";
import Container from "@mui/material/Container";
import Classification from "../components/devices/Classification";
import Copyright from "../components/common/Copyright";
import DevicesGrid from "../components/devices/DevicesGrid";
import Read from "../components/devices/Read";

export default function Devices() {
  return (
    <Container maxWidth="lg" sx={{ my: 2 }}>
      <Read />
      <Classification />
      <DevicesGrid />
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
