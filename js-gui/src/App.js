import React, { Component } from 'react';
import './App.css';
import { connect } from 'react-redux';
import CardColumns from 'react-bootstrap/CardColumns';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { Link } from "react-router-dom";
import Modal from 'react-bootstrap/Modal';
import Image from 'react-image-resizer';
import Grid from './components/Grid';
import Parameters from './components/Parameters';
import Creation from './components/Creation';
import { useState } from 'react';
import tensorboard from './img/tflogo.jpg';
import {
  loadEnvsAction,
  loadEnvsFirebase,
  handleThreed,
  enableModal,
  updateForm
} from './actions';


class App extends Component {

  componentDidMount(){
    this.props.loadEnvsFirebase();
  }

  handleThreed(e){
    const id = e.target.id;
    this.props.handleThreed(id);
  }
  enableModal(e){
    const id = e.target.id;
    this.props.enableModal(id);
  }
  showEnvironment(){
    const { envlist, showenv } = this.props;
    if (showenv){
      this.props.updateForm(envlist[showenv]);
      return (
        <Modal
        size='xl'
        show={true}
        aria-labelledby="example-modal-sizes-title-lg"
        onHide={()=>this.props.enableModal('')}
        animation={false}
        >
        <Modal.Header closeButton>
        <Modal.Title id="example-modal-sizes-title-lg">
        {showenv}
        </Modal.Title>
        </Modal.Header>
        <Parameters preview={true}/>
        </Modal>
      )
    }
  }

  render(){
    const { envlist } = this.props;

    const keys = Object.keys(envlist);
    return (
      <div style={{ padding: '20px' }}>
      <CardColumns >
        {
          keys.map(key => {
            return (
              <Card key={key}>
                <Card.Header >
                  <div style={{ display: 'flex', justifyContent:'center' }}>
                  <Grid
                    preview={300}
                    pheight={envlist[key].height}
                    pwidth={envlist[key].width}
                    pwalls={envlist[key].walls}
                    pinitstate={envlist[key].initstate}
                    pfinalstate={envlist[key].finalstate}
                    />
                  </div>
                </Card.Header>
                <Card.Body>
                  <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-around' }}>
                    <div>
                      <Card.Title style={{ fontWeight: 'bold', fontSize: '26px' }}>{key}</Card.Title>
                      <Button id={key} onClick={this.enableModal.bind(this)} variant="info">Show params</Button>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'center' }}>
                      <Button id={envlist[key].version} onClick={this.handleThreed.bind(this)} style={{ height: "40px", width: "50px" }} variant="warning">3D</Button>
                      <div style={{ overflow: 'hidden', borderRadius: '12px' }}>
                        <a target="_blank" href={"http://localhost:6006/#scalars&_smoothingWeight=0.93&regexInput=".concat(key)}>
                        <Image
                        src={tensorboard}
                        width={50}
                        height={50}
                        /></a>
                      </div>
                    </div>

                  </div>

                </Card.Body>
                <Card.Footer className="text-muted">By admin</Card.Footer>
              </Card>
            )}
          )}
      </CardColumns>
      <div style={{ height: '50px', width: '100%', textAlign: 'center', marginTop: '20px' }}>
      <Link to="/creation">
        <Button
          style={{ height: '100%', width: '100%', fontSize: '20px' }}
          variant="success">
          Create your own environment
        </Button>
      </Link>
      </div>
      {this.showEnvironment()}
      </div>
    );
  }
}

const mapStateToProps = ({ generalbuttons }) => {
  const { envlist, showenv } = generalbuttons;
  return { envlist, showenv };
}


export default connect(mapStateToProps, {
  loadEnvsAction,
  loadEnvsFirebase,
  handleThreed,
  enableModal,
  updateForm
} )(App);
