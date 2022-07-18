import * as React from 'react';
import Frame from "./components/Frame";
import {BrowserRouter} from "react-router-dom";

export default function App() {
    return (
        <BrowserRouter>
            <Frame />
        </BrowserRouter>
    );
}