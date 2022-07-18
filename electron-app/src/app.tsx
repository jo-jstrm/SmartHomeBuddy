import * as React from 'react';
import Frame from "./components/Frame";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Dashboard from "./components/dashboard/Dashboard";
import Devices from "./components/devices/Devices";



export default function App() {
    return (
        <BrowserRouter>
            <Frame />
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/devices" element={<Devices />} />
            </Routes>
        </BrowserRouter>
    );
}