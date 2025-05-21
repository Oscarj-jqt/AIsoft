import Home from "./components/Home";
import Download from "./components/Download";
import { Route, Routes } from "react-router-dom";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/download" element={<Download />} />
    </Routes>
  );
}

export default App;
