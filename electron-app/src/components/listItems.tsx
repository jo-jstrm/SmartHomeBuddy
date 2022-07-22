import * as React from "react";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AssignmentIcon from "@mui/icons-material/Assignment";
import { DeviceUnknown } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

export function MainNavBarItems() {
  const navigate = useNavigate();
  const drawerItems = [
    {
      text: "Home",
      icon: <DashboardIcon />,
      onClick: () => navigate("/home"),
    },
    {
      text: "Identified Devices",
      icon: <DeviceUnknown />,
      onClick: () => navigate("/devices"),
    },
  ];

  return (
    <React.Fragment>
      {drawerItems.map((item, index) => {
        const { text, icon, onClick } = item;
        return (
          <ListItemButton key={index} onClick={onClick}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={text} />
          </ListItemButton>
        );
      })}
    </React.Fragment>
  );
}

export const secondaryListItems = (
  <React.Fragment>
    <ListSubheader component="div" inset>
      Saved reports
    </ListSubheader>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Current month" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Last quarter" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Year-end sale" />
    </ListItemButton>
  </React.Fragment>
);
