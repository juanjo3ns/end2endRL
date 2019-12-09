import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Creation from './components/Creation';
import FirebaseAuth from './components/FirebaseAuth';
import Header from './components/Header';
import { Router, Route } from "react-router-dom";
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import ReduxThunk from 'redux-thunk';
import reducers from './reducers';
import history from './history';


const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
  reducers,
  {},
  composeEnhancers(applyMiddleware(ReduxThunk)));


function Main() {

  return (
    <Provider store={store}>
      <Router history={history}>
        <div style={{ background: "linear-gradient(to bottom,  #CAF0E2,#d5dCf1)" }} id="routes">
          <Header />
          <Route path="/" exact component={App} />
          <Route path="/login" render={(props) => <FirebaseAuth {...props} mainLogin={true} />} />
          <Route path="/creation" component={Creation} />
        </div>
      </Router>
    </Provider>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Main />, rootElement);
