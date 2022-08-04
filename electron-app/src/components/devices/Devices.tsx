import * as React from "react";
import Container from "@mui/material/Container";
import Copyright from "../common/Copyright";
import Title from "../common/Title";
import {Smartphone} from "@mui/icons-material";
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";

export default function Devices() {
    const deviceList = [
        {
            name: "Amazon Echo Dot",
            icon: <Smartphone fontSize="large"/>,
            status: "Identified",
            mac: "00:a0:00:19:2e:01",
            action: <WarningAmberIcon color="action" fontSize="large"/>,
        },
        {
            name: "Google Home Mini",
            icon: <Smartphone fontSize="large"/>,
            status: "Identified",
            mac: "ef:00:49:01:1a:ff",
            action: <WarningAmberIcon color="action" fontSize="large"/>,
        },
    ];
    return (
        <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
            <Title>Devices</Title>
            {deviceList.map((device, index) => {
                const {name, icon, status, mac, action} = device;
                return (
                    <Paper
                        sx={{
                            p: 2,
                            margin: 2,
                            flexGrow: 1,
                            backgroundColor: (theme) =>
                                theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
                        }}
                    >
                        <Grid container direction="row" justifyContent="left" alignItems="center" spacing={2}>
                            <Grid item xs={1} justifyContent="left">
                                {icon}
                            </Grid>
                            <Grid item xs={10} container direction="column" justifyContent="flex-start" spacing={1}>
                                <Grid item xs container justifyContent="flex-start" alignItems="center" spacing={1}>
                                    <Grid item>
                                        <Typography variant="subtitle1">
                                            {name}
                                        </Typography>
                                    </Grid>
                                    <Grid item>
                                        <Typography variant="body2" color="text.secondary">
                                            {mac}
                                        </Typography>
                                    </Grid>
                                </Grid>
                                <Grid item xs container direction="row" spacing={1}>
                                    <Grid item xs>
                                        <Typography gutterBottom variant="body1">
                                            {status}
                                        </Typography>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item xs={1} justifyContent="right">
                                {action}
                            </Grid>
                        </Grid>
                    </Paper>
                );
            })}
            <Copyright sx={{pt: 4}}/>
        </Container>
    );
}
