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
import insight from './img/insight_logo.png';
import sfi from './img/sfi_logo.png';
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
        size='lg'
        show={true}
        aria-labelledby="example-modal-sizes-title-lg"
        onHide={()=>this.props.enableModal('')}
        animation={false}
        backdrop={true}
        animation={true}
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

  privateSession(){
    if (this.props.isSignedIn){
      var path = '/creation';
    }else{
      var path = '/login';
    }

    return (
      <div style={{ height: '50px', width: '100%', textAlign: 'center', marginTop: '20px' }}>
        <Link to={path}>
          <Button
            style={{ height: '100%', width: '100%', fontSize: '20px' }}
            variant="success">
            Create your own environment
          </Button>
        </Link>
      </div>
      )
  }

  render(){
    const { envlist } = this.props;

    const keys = Object.keys(envlist);
    return (
      <div style={{

        paddingLeft: '20px',
        paddingRight: '20px',
        paddingBottom: '20px'}}>

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
                        <a target="_blank" href={"http://18.222.37.215:6006/#scalars&_smoothingWeight=0.93&regexInput=".concat(key)}>
                        <Image
                        src={tensorboard}
                        width={50}
                        height={50}
                        /></a>
                      </div>
                    </div>

                  </div>

                </Card.Body>
                {/*<Card.Footer className="text-muted">By admin</Card.Footer>*/}
              </Card>
            )}
          )}
      </CardColumns>
      {this.privateSession()}

      {this.showEnvironment()}
        <div style={{ paddingLeft: "10px", display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center' }}>
          <Image
          src={insight}
          width={155}
          height={155}
          />
          <Image
          src={sfi}
          width={155}
          height={155}
          />
        </div>
      </div>
    );
  }
}

const mapStateToProps = ({ generalbuttons, auth }) => {
  const { envlist, showenv } = generalbuttons;
  const { isSignedIn } = auth;
  return { envlist, showenv, isSignedIn };
}


export default connect(mapStateToProps, {
  loadEnvsAction,
  loadEnvsFirebase,
  handleThreed,
  enableModal,
  updateForm
} )(App);
