import Home from "./components/Home";
import Analyze from "./components/Analyze";
import { Route, Routes } from "react-router-dom";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/analyze" element={<Analyze />} />
    </Routes>
  );
}

export default App;
