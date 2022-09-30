import * as React from "react";
import { useEffect, useState } from "react";
import { Smartphone } from "@mui/icons-material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Device from "./Device";
import Title from "../common/Title";
import { queryAll } from "../../database/Database";
import { Button, Typography } from "@mui/material";
import { DbDevice, DetectedDevice } from "../../types/DeviceTypes";
import { placeholder_detected_device } from "../common/PlaceholderDevices";

export default function DetectedDevices(props: any) {
  const [devices, setDevices] = useState(placeholder_detected_device);
  const sql = "SELECT * FROM devices";
  const queryDevices = (): void => {
    queryAll(sql)
      .then((rows) => {
        console.log("Received devices: " + rows.toString());
        let devices = rows.map((device: DbDevice): DetectedDevice => {
          console.log(device);
          // TODO improve handling of Icon, status, and action.
          let status = "Identified";
          let action = <></>;
          if (device.device_name == null || device.device_name == "") {
            status = "Not Identified";
            action = <WarningAmberIcon color="action" fontSize="large" />;
          }
          return {
            device_name: device.device_name,
            mac_address: device.mac_address,
            ip_address: device.ip_address,
            icon: <Smartphone fontSize="large" />,
            status: status,
            action: action,
          };
        });
        // Get all unidentified devices.
        devices = devices
          .filter((device: DetectedDevice) => device.status == "Not Identified")
          .slice(0, 5);
        setDevices(devices);
      })
      .catch((err: Error) => {
        console.log("Catch: " + err.toString());
        setDevices(placeholder_detected_device);
      });
  };
  useEffect(() => {
    queryDevices();
  }, []);
  return (
    <React.Fragment>
      <Paper
        sx={{
          p: 2,
          margin: 2,
          flexGrow: 1,
          backgroundColor: (theme) => theme.palette.background.paper,
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
            <Title sx={{ mb: 0 }}>Unidentified Devices</Title>
            <Typography
              m={0}
              py={0}
              sx={{ fontStyle: "italic", fontSize: "0.8rem" }}
            >
              To see a full list of devices use the Devices tab.
            </Typography>
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
            const {
              device_name,
              mac_address,
              ip_address,
              icon,
              status,
              action,
            } = device;
            return (
              <Device
                key={index}
                name={device_name}
                icon={icon}
                status={status}
                mac_address={mac_address}
                ip_address={ip_address}
                action={action}
              />
            );
          })}
        </Grid>
      </Paper>
    </React.Fragment>
  );
}
