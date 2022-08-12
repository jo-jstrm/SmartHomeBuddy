import * as React from "react";
import { createRoot } from "react-dom/client";
import CssBaseline from "@mui/material/CssBaseline";
import Frame from "./views/Frame";
import {HashRouter} from "react-router-dom";

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(
  <React.Fragment>
    {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
    <CssBaseline />
    <HashRouter>
      <Frame />
    </HashRouter>
  </React.Fragment>
);
