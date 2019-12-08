import { combineReducers } from 'redux';
import GeneralReducer from './GeneralReducer';
import FormReducer from './FormReducer';
import EnvsReducer from './EnvsReducer';
import AuthReducer from './AuthReducer';


export default combineReducers({
  auth: AuthReducer,
  generalbuttons: GeneralReducer,
  formValues: FormReducer,
  environments: EnvsReducer
});
