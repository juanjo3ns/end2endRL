import React, { Component } from 'react';
import  { Breakpoint, BreakpointProvider } from 'react-socks';
import { connect } from 'react-redux';
import Button from 'react-bootstrap/Button';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Grid from './Grid';
import Parameters from './Parameters';
import {
  handleClick,
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

  render(){
    console.log(this.state.width);
    return (
      <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch', padding: '12px' }}>
        <BreakpointProvider>
          <Breakpoint medium down>
            <div style={{ display:'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'stretch', padding: '5px' }}>
              <Parameters/>
              <Grid
              preview={this.state.width}
              height={10}
              width={10}
              walls={[]}
              initstate={[]}
              finalstate={[]}
              />
              <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
                <Button onClick={this.handleReset.bind(this)} variant="danger">Reset</Button>
                <ButtonGroup aria-label="Basic example">
                  <Button id="walls" active={this.props.cell==="walls" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Walls</Button>
                  <Button id="initstate" active={this.props.cell==="initstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Init state</Button>
                  <Button id="finalstate" active={this.props.cell==="finalstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Final state</Button>
                </ButtonGroup>
              </div>
            </div>
          </Breakpoint>
          <Breakpoint large up>
            <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch', padding: '5px' }}>
              <Parameters/>
              <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-around" }}>
                <Grid
                preview={700}
                height={10}
                width={10}
                walls={[]}
                initstate={[]}
                finalstate={[]}
                />
                <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-around" }}>
                  <Button onClick={this.handleReset.bind(this)} variant="danger">Reset</Button>
                  <ButtonGroup aria-label="Basic example">
                    <Button id="walls" active={this.props.cell==="walls" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Walls</Button>
                    <Button id="initstate" active={this.props.cell==="initstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Init state</Button>
                    <Button id="finalstate" active={this.props.cell==="finalstate" ? true : false} onClick={this.handleClick.bind(this)} variant="secondary">Final state</Button>
                  </ButtonGroup>
                </div>
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
} )(Creation);
