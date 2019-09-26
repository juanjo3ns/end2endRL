import React, { useState, useContext } from "react";
import { AuthContext } from "../index";
import * as firebase from 'firebase';
import Button from 'react-bootstrap/Button';
import { withRouter } from 'react-router-dom';
import "./Login.css";

const Login = ({history}) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setErrors] = useState("");
  const [activeEmail, setActiveEmail] = useState(false);
  const [lockedEmail, setLockedEmail] = useState(false);

  const [activePass, setActivePass] = useState(false);
  const [lockedPass, setLockedPass] = useState(false);

  const fieldClassNameActive = `field ${(lockedEmail ? activeEmail : activeEmail || email) &&
        "active"} ${lockedEmail && !activeEmail && "locked"}`;
  const fieldClassNameLocked = `field ${(lockedPass ? activePass : activePass || password) &&
        "active"} ${lockedPass && !activePass && "locked"}`;

  const Auth = useContext(AuthContext);
  const handleForm = e => {

    e.preventDefault();
    firebase
    .auth()
    .setPersistence(firebase.auth.Auth.Persistence.SESSION)
      .then(() => {
        firebase
        .auth()
        .signInWithEmailAndPassword(email, password)
        .then(res => {
          if (res.user) Auth.setLoggedIn(true);
          history.push('/creation')
        })
        .catch(e => {
          setErrors(e.message);
        });
      })

  };

  const signInWithGoogle = () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase
    .auth()
    .setPersistence(firebase.auth.Auth.Persistence.SESSION)
    .then(() => {
      firebase
      .auth()
      .signInWithPopup(provider)
      .then(result => {
        console.log(result)
        history.push('/creation')
        Auth.setLoggedIn(true)
      })
      .catch(e => setErrors(e.message))
    })

  }
  return (
    <div
    id="login_form"
    style={{
      background: "linear-gradient(to bottom, #00334D, #673ab7)",
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      width: '100%',
      justifyContent: 'center',
      alignItems: 'center'  }}>

      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1
          onClick={() => history.push('/join')}
          style={{ color: "#198CFF", fontSize: "30px" }}>
          Join
        </h1>
        <h1 style={{ fontWeight: "bold", color: "#198CFF", fontSize: "50px" }}>Login</h1>
      </div>
      <form onSubmit={e => handleForm(e)}>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ padding: '10px' }}>
        <div className={fieldClassNameActive}>

          <input
            id={1}
            type="text"
            value={email}
            placeholder={"Email"}
            onChange={e => setEmail(e.target.value)}
            onFocus={() => !lockedEmail && setActiveEmail(true)}
            onBlur={() => !lockedEmail && setActiveEmail(false)}
          />
          <label htmlFor={1} className={error && "error"}>
            {error || "Email"}
          </label>
        </div>
        </div>
        <div style={{ padding: '10px' }}>
        <div className={fieldClassNameLocked}>

          <input
            id={2}
            type="password"
            value={password}
            placeholder={"Password"}
            onChange={e => setPassword(e.target.value)}
            onFocus={() => !lockedPass && setActivePass(true)}
            onBlur={() => !lockedPass && setActivePass(false)}
          />
          <label htmlFor={1} className={error && "error"}>
            {error || "Password"}
          </label>
        </div>
        </div>
        <div style={{ padding: '10px' }}>
        <Button
        type="submit"
        style={{ fontSize: '20px' }}
        variant="secondary">
        Login
        </Button>
        </div>
        <Button
          onClick={() => signInWithGoogle()}
          type="button"
          className="googleBtn"
          style={{ fontSize: '20px' }}
          variant="secondary">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"
              alt="logo"
            />
            Login with Google

        </Button>

        </div>
      </form>
    </div>
  );
};

export default withRouter(Login);
