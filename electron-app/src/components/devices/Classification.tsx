import * as React from "react";
import {useEffect, useState} from "react";
import {Button, FormControl, InputLabel, MenuItem} from "@mui/material";
import Paper from "@mui/material/Paper";
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Typography from "@mui/material/Typography";
import {styled} from "@mui/system";
import {callClassifyDevices} from "../../rpc/clients/DeviceDatabaseClient";
import {queryAll} from "../../database/Database";
import {DbMeasurement} from "../../types/DeviceTypes";

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
  const classifyDevices = () => {
    setClassifierStatus("Classifying. This might take a moment...");
    const classifierModel = "random_forest"
    callClassifyDevices(classifierModel, selectedMeasurement)
      .then(() => {
        setClassifierStatus("Classified!");
      })
      .catch((err: Error) => {
        console.error("Catch: " + err.toString());
        setClassifierStatus("No response from Device Identifier.");
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
            onClick={classifyDevices}
        >
          Classify Devices
        </Button>
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
              return (<MenuItem key={index} value={measurement}>{measurement}</MenuItem>);
            })}
          </Select>
        </FormControl>
        <Typography>{classifierStatus}</Typography>
      </StyledDiv>
    </StyledPaper>
  );
}
