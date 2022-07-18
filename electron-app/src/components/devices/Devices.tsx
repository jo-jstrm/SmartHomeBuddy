import * as React from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Copyright from "../common/Copyright";
import Device from './Device';

export default function Devices () {
    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
                {/* Recent Orders */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <Device/>
                    </Paper>
                </Grid>
            </Grid>
            <Copyright sx={{ pt: 4 }} />
        </Container>
    );
}
