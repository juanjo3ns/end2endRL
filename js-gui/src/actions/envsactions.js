import {
    FETCH_ENVS_SUCCES,
    FETCH_THREED_SUCCES,
    FETCH_ENV_SUCCES,
    CHANGE_ACTIVE_ENV,
    LOAD_WALLS
} from './types';
import axios from 'axios';


export const fetchEnvironments = () =>  (dispatch) => {
    axios.get("http://localhost:5000/envs")
    .then((response) => {
      dispatch({ type: FETCH_ENVS_SUCCES, payload: response.data });
    });
    axios.get("http://localhost:5000/threedlist")
    .then((response) => {
      dispatch({ type: FETCH_THREED_SUCCES, payload: response.data });
    });
};
export const fetchSingleEnv = (version) => (dispatch) => {
    axios.get("http://localhost:5000/envs", {
    params: {
      version: version
    }}).then((response) => {
      dispatch({ type: FETCH_ENV_SUCCES, payload: response.data });
      const walls = {
        walls: response.data.walls,
        initstate: response.data.initstate,
        finalstate: response.data.finalstate
      }
      dispatch({
        type: LOAD_WALLS,
        payload: walls
      });
    });

  dispatch({
    type: CHANGE_ACTIVE_ENV,
    payload: version.split('.json')[0]
  });
};
