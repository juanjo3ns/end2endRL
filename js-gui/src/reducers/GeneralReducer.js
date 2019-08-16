import {
    CHANGE_BUTTON_CELL,
    UPDATE_CELL_VALUES,
    RESET_CELL_VALUES,
    MOUSE_OVER,
    LOAD_WALLS,
    TRAINING_SUCCESS,
    SET_INTERVAL,
    PROGRESS_UPDATE,
    TRAIN_FINISHED
 } from '../actions/types';

const INITIAL_STATE = {
  cell: "walls",
  walls: [],
  initstate: [],
  finalstate: [],
  walls_values: [],
  clicked: false,
  training: '',
  interval: null,
  progress: 0
};

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case CHANGE_BUTTON_CELL:
            return {...state, cell: action.payload};
        case UPDATE_CELL_VALUES:
            return { ...state, ...action.payload};
        case RESET_CELL_VALUES:
            return { ...state, ...INITIAL_STATE};
        case MOUSE_OVER:
            return { ...state, clicked: action.payload }
        case LOAD_WALLS:
            return { ...state, ...action.payload };
        case TRAINING_SUCCESS:
            return { ...state, training: action.payload };
        case SET_INTERVAL:
            return { ...state, interval: action.payload };
        case PROGRESS_UPDATE:
            return { ...state, progress: action.payload };
        case TRAIN_FINISHED:
            return { ...state, training: '' }
        default:
            return state;
    }
};
