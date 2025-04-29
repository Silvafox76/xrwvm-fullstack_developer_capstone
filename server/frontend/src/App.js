import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";  // <-- Import Register component
import Dealers from './components/Dealers/Dealers';
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} /> {/* <-- Add this route */}
      <Route path="/dealers" element={<Dealers />} />    
    </Routes>
  );
}

export default App;
