import React, { useState ,useEffect ,  useContext  } from "react";
import {useUser} from "./user";
import { useNavigate } from 'react-router-dom';
import {regiser} from "../server"

function Register(props) {
  sessionStorage.clear();
  const [email, setEmail] = useState("");
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); 
  const { user , updateUser  } = useUser();

  // useEffect(() => {
  //   updateUser({ name: "eran", email: "eran@sss.com" });
  // }, []); 
  // console.log("loginuser-- > " , user);

  const handleClick = async (event) => {
  event.preventDefault();
  alert("You clicked the button");
  const res = await regiser({ "username":username, "email":email , "password" :password} , updateUser);
  if (res === true) {
    navigate("/home");
  }
  else{
    alert("email allredy exists");
  }
};

  return (
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="form-group mt-3">
          <label>User Name</label>
            <input
              name="username"
              type="name"
              className="form-control mt-1"
              placeholder="Enter user name"
              value={username}
              onChange={(e) => setUserName(e.target.value)}
            />
          </div>
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
          
         
        </div>
      </form>
    </div>
  );
}

export default Register;
