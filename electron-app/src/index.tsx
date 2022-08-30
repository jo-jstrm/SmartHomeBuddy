import * as React from "react";
import {createRoot} from "react-dom/client";
import Frame from "./views/Frame";
import {HashRouter} from "react-router-dom";

const container = document.getElementById("root");
const root = createRoot(container!);

root.render(
    <HashRouter>
        <Frame/>
    </HashRouter>
);
