// import { createRoot } from 'react-dom/client';
// import { displayText, Props } from './components/displayText'
//
// // Notice the ! -> https://reactjs.org/blog/2022/03/08/react-18-upgrade-guide.html#updates-to-client-rendering-apis
// const container = document.getElementById('root')!
// const root = createRoot(container);
//
// const myText:Props = { text: "Hello from React" }
//
// root.render(displayText(myText));

import * as React from "react";
import Dashboard from "./components/dashboard/Dashboard";

export default function App() {
  return <Dashboard />;
}
