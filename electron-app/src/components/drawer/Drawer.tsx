import {styled} from "@mui/material/styles";
import MuiDrawer from "@mui/material/Drawer";
import {drawerWidth} from "../Globals";
import * as React from "react";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import Divider from "@mui/material/Divider";
import List from "@mui/material/List";
import {MainNavBarItems} from "./DrawerItems";
import shbIcon from '/src/static/assets/shb_icon.png';
import {Box} from "@mui/material";

export const StyledDrawer = styled(MuiDrawer, {
    shouldForwardProp: (prop) => prop !== "open",
})(({theme, open}) => ({
    "& .MuiDrawer-paper": {
        position: "relative",
        whiteSpace: "nowrap",
        width: drawerWidth,
        transition: theme.transitions.create("width", {
            easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    boxSizing: "border-box",
    ...(!open && {
      overflowX: "hidden",
      transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      width: theme.spacing(7),
      [theme.breakpoints.up("sm")]: {
        width: theme.spacing(9),
      },
    }),
  },
}));

export function Drawer(props: { open: boolean; toggleDrawer: () => void }) {
  return (
    <StyledDrawer variant="permanent" open={props.open}>
        <Toolbar
            sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                px: [1],
                height: "64px",
            }}
        >
            <Box sx={{
                mx: 1,
                flexGrow: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-start',
                height: '100%'
            }}>
                <img src={shbIcon} alt="SHB" height="80%"/>
            </Box>
            <IconButton onClick={props.toggleDrawer}>
                <ChevronLeftIcon/>
            </IconButton>
        </Toolbar>
        <Divider/>
      <List component="nav">
        <MainNavBarItems />
      </List>
    </StyledDrawer>
  );
}
