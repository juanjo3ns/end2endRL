import React, { Component } from 'react';
import  { Breakpoint, BreakpointProvider } from 'react-socks';
import { connect } from 'react-redux';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Grid from './Grid';
import Parameters from './Parameters';
import {
  handleClick,
  handleTrain,
  handleReset,
} from '../actions';


class Creation extends Component {

    handleClick(e){
      this.props.handleClick(e.target.id);
    }
    handleReset(e){
      this.props.handleReset();
    }

    constructor(props) {
      super(props);
      this.state = {width: props.width};
    }

    componentWillMount(){
      this.setState({width: window.innerWidth});
    }
    clickTrain(){
      const { formValues, walls, initstate, finalstate, walls_values } = this.props;
      this.props.handleTrain(formValues, walls, initstate, finalstate, walls_values);
    }

    backHome(){
      return(
        <div style={{ padding: '5px' }}>
        <Link to="/">
          <Button
            onClick={this.handleReset.bind(this)}
            style={{ fontSize: '20px' }}
            variant="info">
            HOME
          </Button>
        </Link>
        </div>
      )
    }
    buttonsActions(){
      return(
        <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", alignItems: 'center' }}>
          <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around", padding: "10px" }}>

            <div style={{ padding: "5px" }}>
            <Button onClick={this.handleReset.bind(this)} variant="danger">Reset</Button>
            </div>
            <div style={{ padding: "5px" }}>
            <ButtonGroup aria-label="Basic example">
              <Button id="walls" active={this.props.cell==="walls" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Walls</Button>
              <Button id="initstate" active={this.props.cell==="initstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Init state</Button>
              <Button id="finalstate" active={this.props.cell==="finalstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Final state</Button>
            </ButtonGroup>
            </div>
          </div>
          <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
          {this.backHome()}
          <div style={{ padding: '5px' }}>
            <Link to="/">
              <Button
                onClick={this.clickTrain.bind(this)}
                style={{ fontSize: '20px' }}
                variant="success">
                  TRAIN
              </Button>
            </Link>
          </div>
          </div>
        </div>
      )
    }

  render(){
    return (
      <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch', padding: '10px' }}>
        <BreakpointProvider>
          <Breakpoint medium down>
            <div style={{ display:'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'center' }}>
              <Parameters preview={false}/>
              <Grid
              preview={this.state.width-50}
              height={10}
              width={10}
              walls={[]}
              initstate={[]}
              finalstate={[]}
              />
              {this.buttonsActions()}
            </div>
          </Breakpoint>
          <Breakpoint large up>
            <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch'}}>
              <Parameters preview={false}/>
              <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-around" }}>
                <Grid
                preview={700}
                height={10}
                width={10}
                walls={[]}
                initstate={[]}
                finalstate={[]}
                />
                {this.buttonsActions()}
              </div>
            </div>
          </Breakpoint>
        </BreakpointProvider>
      </div>
    );
  }
}

const mapStateToProps = ({ generalbuttons, formValues }) => {
  const { cell, walls, initstate, finalstate, walls_values } = generalbuttons;
  return { cell, formValues , walls, initstate, finalstate, walls_values };
}

export default connect(mapStateToProps, {
  handleClick,
  handleReset,
  handleTrain
} )(Creation);
