import * as React from "react";
import Container from "@mui/material/Container";
import Copyright from "../common/Copyright";
import Device from "./Device";
import Title from "../common/Title";
import { Stack } from "@mui/material";
import { Smartphone } from "@mui/icons-material";


export default function Devices() {
    const deviceList = [
        {
            name: "Amazon Echo Dot",
            icon: <Smartphone />,
            status: "Identified",
        },
        {
            name: "Google Home Mini",
            icon: <Smartphone />,
            status: "Running",
        },
    ];
    return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Title>Devices</Title>
      <Stack spacing={1}>
        {deviceList.map((device, index) => {
          const { name, icon, status } = device;
          return <Device index={index} name={name} icon={icon} status={status} />;
        })}
      </Stack>
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
