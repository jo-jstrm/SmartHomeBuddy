/**
 * Represents the schema of the device table in the SQLite database.
 */
export interface DeviceType {
  device_name: string;
  mac_address: string;
  ip_address: string;
}