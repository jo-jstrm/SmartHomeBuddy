import * as React from "react";
import { useState } from "react";
import { Smartphone } from "@mui/icons-material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Device from "./Device";
import Title from "../common/Title";
import { queryAll } from "../../database/Database";
import { Button } from "@mui/material";
import { DetectedDevice, DbDevice } from "../../types/DeviceTypes";
import { placeholder_detected_device } from "../common/PlaceholderDevices";

export default function DetectedDevices(props: any) {
  const [devices, setDevices] = useState(placeholder_detected_device);
  const sql = "SELECT * FROM devices LIMIT 5";
  const queryDevices = (): void => {
    queryAll(sql)
      .then((rows) => {
        console.log("Received devices: " + rows.toString());
        let devices = rows.map((device: DbDevice): DetectedDevice => {
          console.log(device);
          // TODO Icon, status, and action are hard coded.
          return {
            device_name: device.device_name,
            mac_address: device.mac_address,
            icon: <Smartphone fontSize="large" />,
            status: "Identified",
            action: <WarningAmberIcon color="action" fontSize="large" />,
          };
        });
        setDevices(devices);
      })
      .catch((err: Error) => {
        console.log("Catch: " + err.toString());
        setDevices(placeholder_detected_device);
      });
  };
  return (
    <React.Fragment>
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
          <Grid item xs={12}>
            <Title {...props}>Devices</Title>
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="outlined"
              size="medium"
              color="primary"
              onClick={queryDevices}
            >
              Load devices from database
            </Button>
          </Grid>
          {devices.map((device, index) => {
            const { device_name, mac_address, icon, status, action } = device;
            return (
              <Device
                key={index}
                name={device_name}
                icon={icon}
                status={status}
                mac_address={mac_address}
                action={action}
              />
            );
          })}
        </Grid>
      </Paper>
    </React.Fragment>
  );
}
