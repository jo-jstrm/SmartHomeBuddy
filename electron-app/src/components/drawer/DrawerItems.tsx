import * as React from "react";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AssignmentIcon from "@mui/icons-material/Assignment";
import {DeviceUnknown} from "@mui/icons-material";
import InsightsIcon from '@mui/icons-material/Insights';
import ShieldIcon from '@mui/icons-material/Shield';
import NotificationImportantIcon from '@mui/icons-material/NotificationImportant';
import ShowChartIcon from '@mui/icons-material/ShowChart';

import {useNavigate} from "react-router-dom";

export function MainNavBarItems() {
  const navigate = useNavigate();
  const drawerItems = [
    {
      text: "Home",
      icon: <DashboardIcon/>,
      onClick: () => navigate("/home"),
    },
    {
      text: "Devices",
      icon: <DeviceUnknown/>,
      onClick: () => navigate("/devices"),
    },
    {
      text: "Network Data",
      icon: <ShowChartIcon/>,
      onClick: () => navigate("/data"),
    },
    {
      text: "Alerts",
      icon: <NotificationImportantIcon/>,
      onClick: () => navigate("/alerts"),
    },
    {
      text: "Countermeasures",
      icon: <ShieldIcon/>,
      onClick: () => navigate("/countermeasures"),
    },
    {
      text: "Insights",
      icon: <InsightsIcon/>,
      onClick: () => navigate("/insights"),
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
      Other Functionalities
    </ListSubheader>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Network Traffic Data" />
    </ListItemButton>
  </React.Fragment>
);
