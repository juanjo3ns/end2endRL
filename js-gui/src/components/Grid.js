import React, { Component } from 'react';
import { connect } from 'react-redux';
import _ from 'lodash';
import { handleCell } from '../actions';


class Grid extends Component {

  handleCell(e){
    const { cell, walls, initstate, finalstate, clicked, walls_values, min_wall, max_wall } = this.props;
    if (e.type === "mouseover" && clicked && cell=== "walls"){
      this.props.handleCell(cell, e.target.id, walls, initstate, finalstate, walls_values, e.type, clicked, min_wall, max_wall);
    }else if (e.type === "click"){
      this.props.handleCell(cell, e.target.id, walls, initstate, finalstate, walls_values, e.type, clicked, min_wall, max_wall);
    }
  }

  getCellStyle(i,j,h,w){
    const { walls, finalstate, initstate } = this.props;
    const id = i.concat("-").concat(j);
    if (walls.indexOf(id)!==-1){
      return {backgroundColor: '#E5A5A5',height: h, width: w,borderRadius: "5px"};
    }else if (initstate.indexOf(id)!==-1){
      return {backgroundColor: '#A5C3E5',height: h, width: w,borderRadius: "5px"};
    }else if (finalstate.indexOf(id)!==-1){
      return {backgroundColor: '#4E4E4E',height: h, width: w,borderRadius: "5px"};
    }else{
      return {backgroundColor: 'rgb(0, 163, 157)',height: h, width: w,borderRadius: "5px"};
    }

  }
  renderCell(cell, i, j){
    const { height, width} = this.props;
    const x = height;
    const y = width;
    const h = (810-(x-1)*7)/x;
    const w = (810-(y-1)*7)/y;
    return (
      <div
      id={i.concat("-").concat(j)}
      className="cell"
      style={this.getCellStyle(i,j,h,w)}
      onClick={this.handleCell.bind(this)}
      onMouseOver={this.handleCell.bind(this)}
      />
    );
  }
  renderRow(row, i){
    return (
      <div key={"row".concat(i)} style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>
      {_.map(row, (t, j) => this.renderCell(t.type, i, j))}
      </div>
    );
  }

  render(){
    return (
      <div style={rootView}>
      {_.map(this.props.gridObject, (t, i) => this.renderRow(t, i)) }
      </div>

    );
  }
}

const rootView = {
  height: "810px",
  width: "810px",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between"
}


const mapStateToProps = ({ formValues, generalbuttons }) => {
  const { cell, walls, initstate, finalstate, clicked, walls_values } = generalbuttons;
  const { height, width, min_wall, max_wall } = formValues;
  var arrX = [...Array(height).keys()];
  var arrY = [...Array(width).keys()];
  var gridObject = _.zipObject(arrX, _.map(arrX, function(){ return _.zipObject(arrY, _.map(arrY, function(){ return {"type":"cell"} }))}));
  return { gridObject, height, width, cell, walls, initstate, finalstate, clicked, walls_values, min_wall, max_wall };
};

export default connect(mapStateToProps, { handleCell })(Grid);
