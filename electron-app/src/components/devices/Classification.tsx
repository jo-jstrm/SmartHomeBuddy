import * as React from "react";
import { useContext, useEffect, useState } from "react";
import {
  Backdrop,
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
} from "@mui/material";
import Paper from "@mui/material/Paper";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/system";
import { callIdentifyDevices } from "../../rpc/clients/DeviceDatabaseClient";
import { queryAll } from "../../database/Database";
import { DbMeasurement } from "../../types/DeviceTypes";
import { FileContext } from "../common/FileContext";

const StyledPaper = styled(Paper)(() => ({
  margin: 10,
  padding: 15,
}));

const StyledDiv = styled("div")(() => ({
  display: "flex",
  justifyContent: "space-between",
  marginBottom: 5,
  alignItems: "center",
}));

export default function Classification() {
  const [classifierStatus, setClassifierStatus] = useState(
    "Classify IoT devices based on the network data in your database."
  );
  const [selectedMeasurement, setSelectedMeasurement] = useState("");
  const [uniqueMeasurements, setUniqueMeasurements] = useState([""]);

  // Backdrop state
  const { devicesBackdrop, setDevicesBackdrop } = useContext(FileContext);

  const identifyDevices = () => {
    // Set backdrop and spinner to loading
    setDevicesBackdrop(true);

    // Classify devices
    setClassifierStatus("Classifying. This might take a moment...");
    const classifierModel = "default";
    callIdentifyDevices(classifierModel, selectedMeasurement)
      .then(() => {
        setClassifierStatus("Classified!");
        setDevicesBackdrop(false);
      })
      .catch((err: Error) => {
        console.error("Catch (callIdentifyDevices): " + err.toString());
        setClassifierStatus(
          "callIdentifyDevices: No response from Device Identifier."
        );
        setDevicesBackdrop(false);
      });
  };
  const queryMeasurements = (): void => {
    const query = "SELECT DISTINCT measurement from devices";
    queryAll(query)
      .then((rows: DbMeasurement[]): void => {
        const measurements = rows.map((measurement: DbMeasurement): string => {
          return measurement.measurement;
        });
        console.log("Measurements: " + measurements);
        setUniqueMeasurements(measurements);
      })
      .catch((err: Error) => {
        console.error("Catch: " + err.toString());
      });
  };
  const handleMeasurement = (event: SelectChangeEvent) => {
    setSelectedMeasurement(event.target.value as string);
  };
  useEffect(() => {
    queryMeasurements();
  }, []);
  return (
    <StyledPaper>
      <StyledDiv>
        <Button
          variant="outlined"
          size="medium"
          color="secondary"
          onClick={identifyDevices}
        >
          Classify Devices
        </Button>
        <Backdrop
          sx={{
            color: (theme) => theme.palette.primary.contrastText,
            zIndex: (theme) => theme.zIndex.fab,
          }}
          open={devicesBackdrop}
          onClick={() => setDevicesBackdrop(false)}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel id="measurement-select-label">Measurement</InputLabel>
          <Select
            labelId="measurement-select-label"
            id="measurement-select"
            value={selectedMeasurement}
            label="Measurement"
            onChange={handleMeasurement}
          >
            {uniqueMeasurements.map((measurement, index) => {
              return (
                <MenuItem key={index} value={measurement}>
                  {measurement}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
        <Typography>{classifierStatus}</Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
