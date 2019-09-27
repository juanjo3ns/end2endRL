import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Creation from './components/Creation';
import Login from './components/Login';
import Join from './components/Join';
import { HashRouter as Router, Route } from "react-router-dom";
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import ReduxThunk from 'redux-thunk';
import reducers from './reducers';
import history from './history';

const store = createStore(reducers, {}, applyMiddleware(ReduxThunk));

export const AuthContext = React.createContext(null);


function Main() {
  const [isLoggedIn, setLoggedIn] = useState(false);

  return (
    <AuthContext.Provider value={{ isLoggedIn, setLoggedIn }}>
      <Provider store={store}>
        <Router history={history}>
          <div id="routes">
            <Route path="/" exact component={App} />
            <Route path="/login" component={Login} />
            <Route path="/join" component={Join} />
            <Route path="/creation" component={Creation} />
          </div>
        </Router>
      </Provider>
    </AuthContext.Provider>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Main />, rootElement);
