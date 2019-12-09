import React, { Component } from 'react';
import  { Breakpoint, BreakpointProvider } from 'react-socks';
import { connect } from 'react-redux';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Grid from './Grid';
import Snackbar from '@material-ui/core/Snackbar';
import MySnackbarContentWrapper from './WrapperSnackBar';
import Parameters from './Parameters';
import {
  handleClick,
  handleTrain,
  handleReset,
  handleSnackClose
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
      const { formValues, walls, initstate, finalstate, walls_values, auth } = this.props;
      this.props.handleTrain(formValues, walls, initstate, finalstate, walls_values, auth);
    }
    handleClose(){
      this.props.handleSnackClose();
    }

    renderSnackBar(){
      const { snackopen, snackvariant, snackmessage } = this.props;
      return (
        <Snackbar
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        open={snackopen}
        autoHideDuration={6000}
        onClose={this.handleClose.bind(this)}
      >
        <MySnackbarContentWrapper
          onClose={this.handleClose.bind(this)}
          variant={snackvariant}
          message={snackmessage}
        />
      </Snackbar>
      )
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
              <Button
                onClick={this.clickTrain.bind(this)}
                style={{ fontSize: '20px' }}
                variant="success">
                  TRAIN
              </Button>
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
        {this.renderSnackBar()}
      </div>
    );
  }
}

const mapStateToProps = ({ generalbuttons, formValues, auth }) => {
  const { cell, walls, initstate, finalstate, walls_values, snackopen, snackvariant, snackmessage } = generalbuttons;
  return { auth, cell, formValues , walls, initstate, finalstate, walls_values, snackopen, snackvariant, snackmessage };
}

export default connect(mapStateToProps, {
  handleClick,
  handleReset,
  handleTrain,
  handleSnackClose
} )(Creation);
