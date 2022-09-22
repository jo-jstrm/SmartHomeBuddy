import * as React from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import { Drawer } from "../components/drawer/Drawer";
import { AppBar } from "../components/AppBar";
import { Route, Routes, useLocation } from "react-router-dom";
import Home from "./Home";
import Devices from "./Devices";
import Data from "./Data";
import Alerts from "./Alerts";
import Countermeasures from "./Countermeasures";
import Insights from "./Insights";
import Settings from "./Settings";
import { route_titles } from "../components/Globals";
import { SwitchModeButton } from "../components/common/SwitchModeButton";
import { ColorContext } from "../themes/ColorContext";
import { PaletteMode } from "@mui/material";
import { lightTheme } from "../themes/light";
import { darkTheme } from "../themes/dark";

function FrameContent() {
  const [mode, setMode] = React.useState<PaletteMode>("light");

  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode: PaletteMode) =>
          prevMode === "light" ? "dark" : "light"
        );
      },
    }),
    []
  );

  const theme = React.useMemo(
    () => createTheme(mode === "light" ? lightTheme : darkTheme),
    [mode]
  );

  const [open, setOpen] = React.useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <ColorContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline enableColorScheme />
        <Box sx={{ display: "flex" }}>
          <AppBar
            position="absolute"
            open={open}
            color="primary"
            enableColorOnDark
          >
            <Toolbar
              sx={{
                pr: "24px", // keep right padding when drawer closed
                height: "64px",
              }}
            >
              <IconButton
                edge="start"
                color="inherit"
                aria-label="open drawer"
                onClick={toggleDrawer}
                sx={{
                  marginRight: "36px",
                  ...(open && { display: "none" }),
                }}
              >
                <MenuIcon />
              </IconButton>
              <Typography
                component="h1"
                variant="h6"
                color="inherit"
                noWrap
                sx={{ flexGrow: 1 }}
              >
                {route_titles[useLocation().pathname]}
              </Typography>
              <SwitchModeButton />
            </Toolbar>
          </AppBar>
          <Drawer open={open} toggleDrawer={toggleDrawer} />
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              height: "100vh",
              overflow: "auto",
            }}
          >
            <Toolbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/main_window" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/devices" element={<Devices />} />
              <Route path="/data" element={<Data />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/countermeasures" element={<Countermeasures />} />
              <Route path="/insights" element={<Insights />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>
      </ThemeProvider>
    </ColorContext.Provider>
  );
}

export default function Frame() {
  return <FrameContent />;
}
