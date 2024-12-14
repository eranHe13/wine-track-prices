import React , {useEffect  , useState} from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Navigate } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import './App.css';
import LogIn from './login' ;
import Home from './home' ; 
import Register from './register';
import { UserProvider ,useUser } from './user'; // Adjust the path as needed


function App() {
  const [user, setUser] = useState({isLogged:false});
  return (
    <UserProvider>
    <BrowserRouter>
    <Routes>
      <Route path="/login" element={!user.isLogged ? <LogIn /> : <Navigate replace to="/home" />} />
      <Route path="/home" element={ <Home /> } />
      <Route path="/Register" element={ <Register /> } />
      <Route path="/" element={<Navigate replace to={user.isLogged ? "/home" : "/login"} />} />
    </Routes>
  </BrowserRouter>
  </UserProvider>
  );
}
  
export default App;

