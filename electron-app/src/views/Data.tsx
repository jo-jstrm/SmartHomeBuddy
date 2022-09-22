import * as React from "react";
import Container from "@mui/material/Container";
import Copyright from "../components/common/Copyright";
import { Read } from "../components/data/Read";

export default function Data() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Read />
      <Copyright sx={{ pt: 4 }} />
    </Container>
  );
}
