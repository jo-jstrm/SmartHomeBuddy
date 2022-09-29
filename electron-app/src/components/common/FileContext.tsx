import { createContext } from "react";

export const FileContext = createContext({
  devicesBackdrop: false,
  setDevicesBackdrop: (bool: boolean) => {},
});
