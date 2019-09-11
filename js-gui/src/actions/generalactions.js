import React from 'react';
import {
  LOAD_ENVS_SUCCESS,
  CHANGE_BUTTON_CELL,
  UPDATE_CELL_VALUES,
  RESET_CELL_VALUES,
  RESET_ENV,
  RESET_FORM,
  FETCH_ENVS_SUCCES,
  CHANGE_ACTIVE_ENV,
  MOUSE_OVER,
  TRAINING_SUCCESS,
  SET_INTERVAL,
  PROGRESS_UPDATE,
  TRAIN_FINISHED,
  ENABLE_MODAL,
  UPDATE_SUCCESS
} from './types';
import loadEnvs from '../requests/envs';
import toaster from 'toasted-notes';
import 'toasted-notes/src/styles.css';
import axios from 'axios';
import base_url from '../requests/base_url';
import db from '../config';


const validateValues = (formValues, walls, walls_values, initstate, finalstate) => {
  Object.entries(formValues).map(([key, value]) => {
    if (
      key === "savefreq" ||
      key === "iterations" ||
      key === "visibleRad" ||
      key === "normal_reward" ||
      key === "min_wall" ||
      key === "max_wall" ||
      key === "seed" ||
      key === "done_reward" ||
      key === "edge_value" ||
      key === "numAgents" ||
      key === "epsmax" ||
      key === "epsmin" ||
      key === "health"
    ) {
      if (isNaN(value)) {
        return [false, 'Incorrect values!'];
      }
    } else if (
      key === "numwalls" ||
      key === "batch_size" ||
      key === "pos" ||
      key === "variance"
    ) {
      if (isNaN(value.value)) {
        return [false, 'Incorrect values!'];
      }
    }
  });
  if ((initstate.length === 0 || finalstate.length === 0) && (formValues.alg === "DQN" || formValues.alg === "GA")) {
    return [false, 'Add initial and final state!']
  }
  return [true, ''];
}


export const loadEnvsFirebase = () => dispatch => {
  db.collection("envs").doc("1xrCYPCUrzwPTHOwjoJe").onSnapshot(doc => {
    dispatch({
      type: LOAD_ENVS_SUCCESS,
      payload: doc.data()
    });
  });
}


export const loadEnvsAction = () => dispatch => {
  base_url.get('/allenvs')
    .then((response) => {
      dispatch({
        type: LOAD_ENVS_SUCCESS,
        payload: response.data
      });
    });
}


export const enableModal = version => {
  return {
    type: ENABLE_MODAL,
    payload: version
  }
}

export const updateForm = values => {
  return {
    type: UPDATE_SUCCESS,
    payload: values
  }
}


export const saveEnv = (formValues, walls, initstate, finalstate, walls_values) => dispatch => {
  const a = validateValues(formValues, walls, walls_values, initstate, finalstate);
  const able = a[0];
  const comment = a[1];
  if (able) {
    const data = {
      ...formValues,
      walls: walls,
      initstate: initstate,
      finalstate: finalstate,
      walls_values: walls_values
    };
    axios.post("http://localhost:5000/envs", data)
      .then((response) => {
        toaster.notify(() => {
          return ( < div style = {
              {
                backgroundColor: 'white',
                padding: "10px",
                borderRadius: "10px"
              }
            } >
            <
            span style = {
              {
                fontSize: "20px"
              }
            } > Environment saved! < /span> <
            /div>
          )
        });
        dispatch({
          type: CHANGE_ACTIVE_ENV,
          payload: formValues.version
        });
        dispatch({
          type: FETCH_ENVS_SUCCES,
          payload: response.data
        });
      });
  } else {

    toaster.notify(() => {
      return ( < div style = {
          {
            backgroundColor: 'white',
            padding: "10px",
            borderRadius: "10px"
          }
        } >
        <
        span style = {
          {
            fontSize: "20px"
          }
        } > {
          comment
        } < /span> <
        /div>
      )
    });
    toaster.notify(() => {
      return ( < div style = {
          {
            backgroundColor: 'white',
            padding: "10px",
            borderRadius: "10px"
          }
        } >
        <
        span style = {
          {
            fontSize: "20px"
          }
        } > {
          comment
        } < /span> <
        /div>
      )
    });
  }
};

export const trainFinished = () => {
  return {
    type: TRAIN_FINISHED,
    payload: ''
  }
}

export const requestProgress = (dispatch) => {
  axios.get("http://localhost:5000/progress")
    .then((response) => {
      dispatch({
        type: PROGRESS_UPDATE,
        payload: response.data
      });
    });
}

export const handleTrain = (version) => (dispatch) => {
  version = version.concat('.json');
  axios.get("http://localhost:5000/train", {
      params: {
        version: version
      }
    })
    .then((response) => {
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data.comment
          } < /span> <
          /div>
        )
      });

      if (response.data.training) {
        dispatch({
          type: TRAINING_SUCCESS,
          payload: version
        });
        const intervalID = setInterval(() => {
          requestProgress(dispatch);
        }, 5000);
        dispatch({
          type: SET_INTERVAL,
          payload: intervalID
        });
      }

    });
}

export const handleStop = () => dispatch => {
  axios.get("http://localhost:5000/kill")
    .then((response) => {
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });

    });
}

export const handleEval = (version) => (dispatch) => {
  version = version.concat('.json');
  axios.get("http://localhost:5000/eval", {
      params: {
        version: version
      }
    })
    .then((response) => {
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });

    });
}

export const handleDel = (version) => (dispatch) => {
  axios.get("http://localhost:5000/del", {
      params: {
        version: version
      }
    })
    .then((response) => {
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data
          } < /span> <
          /div>
        )
      });
    });
  axios.get("http://localhost:5000/envs")
    .then((response) => {
      dispatch({
        type: FETCH_ENVS_SUCCES,
        payload: response.data
      });
    });
  dispatch({
    type: RESET_CELL_VALUES,
    payload: "reset"
  });
  dispatch({
    type: RESET_ENV,
    payload: "reset"
  });
  dispatch({
    type: RESET_FORM,
    payload: "reset"
  });
}

export const handleThreed = (version) => (dispatch) => {
  version = version
  const algorithm = version.split('.')[0];
  axios.get("http://localhost:5000/threed", {
      params: {
        version: version,
        algorithm: algorithm
      }
    })
    .then((response) => {
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data.comment
          } < /span> <
          /div>
        )
      });
      toaster.notify(() => {
        return ( < div style = {
            {
              backgroundColor: 'white',
              padding: "10px",
              borderRadius: "10px"
            }
          } >
          <
          span style = {
            {
              fontSize: "20px"
            }
          } > {
            response.data.comment
          } < /span> <
          /div>
        )
      });
      if (response.data.exists) {
        if (algorithm === "DQN") {
          window.open('http://localhost:5000/threeddqn', "_blank");
        } else if (algorithm === "GA") {
          window.open('http://localhost:5000/threedga', "_blank");
        } else if (algorithm === "RWB") {
          window.open('http://localhost:5000/threedpgm', "_blank");
        } else if (algorithm === "A2C") {
          window.open('http://localhost:5000/threedac', "_blank");
        }
      }

    });


}

export const handleClick = (id) => {
  return {
    type: CHANGE_BUTTON_CELL,
    payload: id
  };
};

export const handleCell = (cell, id, walls, initstate, finalstate, walls_values, type, clicked, min_wall, max_wall) => dispatch => {
  if (type === "click" && cell === "walls") {
    dispatch({
      type: MOUSE_OVER,
      payload: !clicked
    });
  }
  if (walls.indexOf(id) !== -1) {
    const index = walls.indexOf(id);
    walls_values.splice(index, 1);
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        walls: walls.filter((wall) => {
          return wall !== id
        }),
        walls_values: [...walls_values]
      }
    });
  } else if (initstate.indexOf(id) !== -1) {
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        initstate: []
      }
    });
  } else if (finalstate.indexOf(id) !== -1) {
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        finalstate: []
      }
    });
  } else if (cell === "finalstate") {
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        finalstate: [id]
      }
    });
  } else if (cell === "initstate") {
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        initstate: [id]
      }
    });
  } else {
    dispatch({
      type: UPDATE_CELL_VALUES,
      payload: {
        walls: [...walls, id],
        walls_values: [...walls_values, Math.random() * (max_wall - min_wall) + min_wall]
      }
    });
  }
};

export const handleReset = () => (dispatch) => {
  dispatch({
    type: RESET_CELL_VALUES,
    payload: "reset"
  });
  dispatch({
    type: RESET_ENV,
    payload: "reset"
  });
  dispatch({
    type: RESET_FORM,
    payload: "reset"
  });
};
