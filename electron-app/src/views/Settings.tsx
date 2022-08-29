import * as React from "react";
import Container from "@mui/material/Container";
import Copyright from "../components/common/Copyright";


export default function Settings() {
    return (
        <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
            <Copyright sx={{pt: 4}}/>
        </Container>
    );
}