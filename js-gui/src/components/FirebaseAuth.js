import React, { Component } from 'react';
import { connect } from 'react-redux';
import { signIn, signOut } from '../actions';
import * as firebase from 'firebase';


class GoogleAuth extends Component {

  componentDidMount(){
    firebase.auth().onAuthStateChanged((user) => {
        if (user) {
          this.props.signIn(user.uid);
          this.props.getUserIds(user.uid);
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
          this.props.signIn(result.user.uid);
        })
        .catch(e => console.log(e.message))
      });
    }

  onSignOutClick(){
    firebase.auth().signOut().then(() => {
      this.props.signOut();
    }).catch(e => {
      console.log(e.message);
    });
  }



  renderAuthButton() {
    if (this.props.isSignedIn === null){
      return null;
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
