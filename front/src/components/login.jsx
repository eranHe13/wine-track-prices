import React, { useState ,useEffect ,  useContext  } from "react";
import {useUser} from "./user";
import { useNavigate } from 'react-router-dom';
import {login_server} from "../server"
import image from "./assests/login.jpg";

function LogIn(props) {
  sessionStorage.clear();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // Initialize useNavigate hook
  const { user , updateUser  } = useUser();

  const handleClick = async (event) => {
  event.preventDefault();
  alert("You clicked the button");
  const res = await login_server({"email":email , "password" :password} , updateUser);
  if (res === true) {
    
    navigate("/home");
  }
  else{
    alert("user details not correct");
  }
};

const handleClickRegister = async (event) => {
  event.preventDefault();
  navigate("/register");
};

  return (
    <div style={{display : "flex" , alignItems:"center" }}>
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign In</h3>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              name="Email"
              type="email"
              className="form-control mt-1"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              name="pass"
              type="password"
              className="form-control mt-1"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary" onClick={handleClick} >
              Submit
            </button>
          </div>
          <div className="d-grid gap-2 mt-3">
            <button className="btn btn-primary" onClick={handleClickRegister} >
              Register
            </button>
            
          </div>
         
        </div>
      </form>
      <img src={image} style={{height:"500px" , width:"500px" , borderRadius:"20%"}}/>

    </div>
    </div>
  );
}

export default LogIn;
