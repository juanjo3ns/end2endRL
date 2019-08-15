import {
    CHANGE_BUTTON_CELL,
    UPDATE_CELL_VALUES,
    RESET_CELL_VALUES,
    MOUSE_OVER,
    LOAD_WALLS
 } from '../actions/types';

const INITIAL_STATE = {
  cell: "walls",
  walls: [],
  initstate: [],
  finalstate: [],
  walls_values: [],
  clicked: false
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
            return { ...state, ...action.payload }
        default:
            return state;
    }
};
