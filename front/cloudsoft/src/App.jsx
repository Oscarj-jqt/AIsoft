import Home from "./components/Home";
import Analyze from "./components/Analyze";
import Arme from "./components/Arme";
import Login from "./components/Login";
import Register from "./components/Register";
import { Route, Routes } from "react-router-dom";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/analyze" element={<Analyze />} />
      <Route path="/arme" element={<Arme />} />
      <Route path="/home" element={<Home />}/>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

export default App;
