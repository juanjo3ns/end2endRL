import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { connect } from 'react-redux';
import Button from 'react-bootstrap/Button';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import toaster from 'toasted-notes';
import 'toasted-notes/src/styles.css';
import Parameters from './components/Parameters';
import Grid from './components/Grid';
import Environments from './components/Environments';
import {
  saveEnv,
  handleClick,
  handleReset,
  handleTrain,
  handleEval,
  handleThreed,
  handleDel
} from './actions';


class App extends Component {

  onButtonPress() {
      this.props.saveEnv();
  }
  handleClick(e){
    this.props.handleClick(e.target.id);
  }
  handleReset(e){
    this.props.handleReset();
  }
  onClickSave(e){
    const { formValues, walls, initstate, finalstate, walls_values } = this.props;
    this.props.saveEnv(formValues, walls, initstate, finalstate, walls_values);
  }
  checkActiveEnv(callback){
    if (this.props.activenv === ''){
      toaster.notify(() => {
        return(<div style={{ backgroundColor: 'white', padding: "10px", borderRadius: "10px" }}>
          <span style={{ fontSize: "20px" }}>Select environment!</span>
        </div>
      )});
      toaster.notify(() => {
        return(<div style={{ backgroundColor: 'white', padding: "10px", borderRadius: "10px" }}>
          <span style={{ fontSize: "20px" }}>Select environment!</span>
        </div>
      )});
    }else{
      callback(this.props.activenv);
    }
  }
  onClickTrain(e){
    this.checkActiveEnv(this.props.handleTrain);
  }
  onClickEval(e){
    this.checkActiveEnv(this.props.handleEval);
  }
  onClickThreed(e){
    this.checkActiveEnv(this.props.handleThreed);
  }
  onClickDel(e){
    this.checkActiveEnv(this.props.handleDel);
  }

  render(){
    return (
      <div className="App" style={{ display: 'flex', justifyContent: 'space-around' }}>
      <div style={Boxes}>
        <div>
        <Parameters />
        </div>
        <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
          <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
          <Button onClick={this.handleReset.bind(this)} variant="danger">Reset</Button>
          <ButtonGroup aria-label="Basic example">
            <Button id="walls" active={this.props.cell==="walls" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Walls</Button>
            <Button id="initstate" active={this.props.cell==="initstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Init state</Button>
            <Button id="finalstate" active={this.props.cell==="finalstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Final state</Button>
          </ButtonGroup>
          </div>
        <Grid />
        <ButtonToolbar style={{ width: "100%", justifyContent: "space-around" }}>
          <Button variant="primary" onClick={this.onClickSave.bind(this)} size="lg">SAVE</Button>
          <Button variant="primary" onClick={this.onClickTrain.bind(this)} size="lg">TRAIN</Button>
          <Button variant="primary" onClick={this.onClickEval.bind(this)} size="lg">EVAL</Button>
          <Button variant="warning" onClick={this.onClickThreed.bind(this)} size="lg">3D</Button>
          <Button variant="danger" onClick={this.onClickDel.bind(this)} size="lg">DELETE</Button>
        </ButtonToolbar>
        </div>
        <div>
        <Environments/>
        </div>
      </div>
      </div>
    );
  }

}

const Boxes = {
  display: "flex",
  flexDirection: "row",
  alignItems: "stretch",
  justifyContent: "space-around",
  width: "100%",
  height: "100%",
  padding: "2px",
}

const mapStateToProps = ({ generalbuttons, formValues, environments }) => {
  const { cell, walls, initstate, finalstate, walls_values } = generalbuttons;
  const { activenv } = environments;
  return { cell, formValues , walls, initstate, finalstate, walls_values, activenv };
}

export default connect(mapStateToProps, {
  saveEnv,
  handleClick,
  handleReset,
  handleTrain,
  handleEval,
  handleThreed,
  handleDel
} )(App);