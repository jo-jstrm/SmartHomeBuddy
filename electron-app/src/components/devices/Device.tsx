import * as React from "react";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

export const DeviceContent = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  color: theme.palette.text.secondary,
  elevation: 2,
}));

export default function Device(props: {
  name: string;
  icon: any;
  status: string;
}) {
  return (
    <DeviceContent>
      <Stack direction="row" alignItems="center" gap={1}>
        {props.icon}
        <Typography variant="h5">{props.name}</Typography>
        <Typography variant="body1">{props.status}</Typography>
      </Stack>
    </DeviceContent>
  );
}
