import {
  SIGN_IN,
  SIGN_OUT
 } from '../actions/types';

const INITIAL_STATE = {
  isSignedIn: false,
  email: null,
  uid: null,
  name: null
};

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case SIGN_IN:
            return { ...state, isSignedIn: true, ...action.payload };
        case SIGN_OUT:
            return { ...state, ...INITIAL_STATE }
        default:
            return state;
    }
};
