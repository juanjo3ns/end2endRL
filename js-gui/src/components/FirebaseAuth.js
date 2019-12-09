import React, { Component } from 'react';
import { connect } from 'react-redux';
import { signIn, signOut } from '../actions';
import Button from 'react-bootstrap/Button';
import history from '../history';
import * as firebase from 'firebase';


class GoogleAuth extends Component {

  componentDidMount(){
    firebase.auth().onAuthStateChanged((user) => {
        if (user) {
          this.props.signIn(user);
        } else {
          this.props.signOut();
        }
      });
  }

  signInWithGoogle(){
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL)
      .then(() => {
        firebase.auth().signInWithPopup(provider)
        .then(result => {
          history.push('/creation');
          this.props.signIn(result.user);

        })
        .catch(e => console.log(e.message))
      });
    }

  onSignOutClick(){
    firebase.auth().signOut().then(() => {
      this.props.signOut();
      history.push('/')
    }).catch(e => {
      console.log(e.message);
    });
  }



  renderAuthButton() {
    if (this.props.isSignedIn === null){
      return null;
    } else if(this.props.mainLogin) {
        return(
          <div id="login" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%', height: '100%' }}>
            <Button
              onClick={this.signInWithGoogle.bind(this)}
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
      )
    } else if(this.props.isSignedIn){
      return(
          <button onClick={this.onSignOutClick.bind(this)} className="ui blue basic button">
            <i className="google icon" />
              Sign out
          </button>
      )
    } else{
      return (
        <button onClick={this.signInWithGoogle.bind(this)} className="ui blue basic button">
          <i className="google icon" />
            Sign in
        </button>
      )
    }
  }

  render(){
    return(
      <div>{this.renderAuthButton()}</div>
    );
  }
}

const mapStateToProps = ({ auth }) => {
  const { isSignedIn } = auth;
  return { isSignedIn };
}

export default connect(mapStateToProps, {
  signIn,
  signOut
})(GoogleAuth);
