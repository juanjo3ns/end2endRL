import {
    SIGN_IN,
    SIGN_OUT
} from './types';

export const signIn = user => {
  return {
    type: SIGN_IN,
    payload: {
      email: user.email,
      name: user.displayName,
      uid: user.uid
     }
  }
}

export const signOut = () => {
  return {
    type: SIGN_OUT
    }
}
