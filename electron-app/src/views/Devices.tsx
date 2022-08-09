import * as React from "react";
import Container from "@mui/material/Container";
import Copyright from "../components/common/Copyright";
import Title from "../components/common/Title";
import { Smartphone } from "@mui/icons-material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import Device from "../components/Device";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";

export default function Devices() {
  const deviceList = [
    {
      name: "Amazon Echo Dot",
      icon: <Smartphone fontSize="large" />,
      status: "Identified",
      mac: "00:a0:00:19:2e:01",
      action: <WarningAmberIcon color="action" fontSize="large" />,
    },
    {
      name: "Google Home Mini",
      icon: <Smartphone fontSize="large" />,
      status: "Identified",
      mac: "ef:00:49:01:1a:ff",
      action: <WarningAmberIcon color="action" fontSize="large" />,
    },
  ];
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Title>Devices</Title>
      <Paper
        sx={{
          p: 2,
          margin: 2,
          flexGrow: 1,
          backgroundColor: (theme) =>
            theme.palette.mode === "dark" ? "#1A2027" : "#fff",
        }}
      >
        <Grid
          container
          direction="row"
          justifyContent="left"
          alignItems="center"
          spacing={2}
        >
          {deviceList.map((device, index) => {
            const { name, icon, status, mac, action } = device;
            return (
              <Device
                index={index}
                name={name}
                icon={icon}
                status={status}
                mac={mac}
                action={action}
              />
            );
          })}
        </Grid>
      </Paper>
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
