import { spawn } from "child_process";
import path from "path";

export function runDeviceIdentifier(): void {
  // Handle different location of the device-identifier binary
  const isDevMode = process.env.DEV_MODE
    ? process.env.DEV_MODE.trim() == "true"
    : false;
  console.log("DEV_MODE=" + isDevMode);
  if (isDevMode) {
    return;
  }
  const deviceIdentifierPath = path.join(process.resourcesPath, "device_identifier_server/device_identifier_server");
  console.log("deviceIdentifierPath: " + deviceIdentifierPath);
  let child = spawn(deviceIdentifierPath);
}