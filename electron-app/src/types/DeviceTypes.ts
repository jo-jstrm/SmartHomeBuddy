/**
 * Represents the schema of the device table in the SQLite database.
 * Attention: Changes to the database schema must be reflected here and vice versa.
 */
export interface DbDevice {
  id: number
  device_name: string;
  mac_address: string;
  ip_address: string;
}

/**
 * Contains all information required for displaying a detected device, e.g., in the home view.
 */
export interface DetectedDevice {
  device_name: string;
  mac_address: string;
  icon: JSX.Element;
  status: string;
  action: JSX.Element;
}