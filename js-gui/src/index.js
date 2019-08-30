import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Creation from './components/Creation';
import { HashRouter as Router, Route } from "react-router-dom";
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import ReduxThunk from 'redux-thunk';
import reducers from './reducers';

const store = createStore(reducers, {}, applyMiddleware(ReduxThunk));

ReactDOM.render(

      <Provider store={store}>
        <Router>
          <div>
            <Route path="/" exact component={App} />
            <Route path="/creation" component={Creation} />
          </div>
        </Router>
      </Provider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
