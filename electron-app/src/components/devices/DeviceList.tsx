import * as React from "react";
import {useState} from "react";
import {Smartphone} from "@mui/icons-material";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Device from "./Device";
import Title from "../common/Title";
import {queryAll} from "../../database/Database";
import {Button} from "@mui/material";


const deviceList = [
  {
    name: "Amazon Echo Dot",
    icon: <Smartphone fontSize="large" />,
    status: "Identified",
    mac_address: "00:a0:00:19:2e:01",
    action: <WarningAmberIcon color="action" fontSize="large" />,
  },
  {
    name: "Google Home Mini",
    icon: <Smartphone fontSize="large" />,
    status: "Identified",
    mac_address: "ef:00:49:01:1a:ff",
    action: <WarningAmberIcon color="action" fontSize="large" />,
  },
];

const dummy_devices = [
  {
    name: "Default Device",
    mac_address: "00:00:00:00:00:00",
    icon: <Smartphone fontSize="large" />,
    status: "Not Identified",
    action: <WarningAmberIcon color="action" fontSize="large" />,
  },
  {
    name: "Another Default Device",
    mac_address: "00:00:00:00:00:00",
    icon: <Smartphone fontSize="large" />,
    status: "Not Identified",
    action: <WarningAmberIcon color="action" fontSize="large" />,
  }
]

export default function DeviceList(props: any) {
  const [devices, setDevices] = useState(dummy_devices);
  const sql = "SELECT * FROM devices";
  const queryDevices = () => {
    queryAll(sql)
      .then((rows) => {
        console.log("Received devices: " + rows.toString())
        let devices = rows.map((elem: { device_name: string, mac_address: string }) => {
          console.log(elem)
          // TODO Icon, status, and action are hard coded.
          return {
            name: elem.device_name,
            mac_address: elem.mac_address,
            icon: <Smartphone fontSize="large" />,
            status: "Identified",
            action: <WarningAmberIcon color="action" fontSize="large" />,
          }
        })
        setDevices(devices)
      })
      .catch((err: Error) => {
        console.log("Catch: " + err.toString())
        setDevices(dummy_devices)
      })
  }
  return (
    <React.Fragment>
      <Title {...props} >Devices</Title>
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
            <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
              <Button onClick={queryDevices}>
                 Load devices from database
              </Button>
            </Paper>
          </Grid>
          {devices.map((device, index) => {
            const { name, mac_address, icon, status, action } = device;
            return (
              <Device
                key={index}
                name={name}
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