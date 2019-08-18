import React, { Component } from 'react';
import { connect } from 'react-redux';

import Form from 'react-bootstrap/Form';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';

import Slider from 'rc-slider/lib/Slider';
import 'rc-slider/assets/index.css';

import { heightSlider,
  widthSlider,
  changeAlgorithm,
  changeInput,
  changeCheck } from '../actions';


class Parameters extends Component {

  heightChanged(value) {
    this.props.heightSlider(value);
  }
  widthChanged(value) {
    this.props.widthSlider(value);
  }
  // componentDidMount() {
  //     this.props.heightSlider();
  //     this.props.widthSlider();
  //     this.props.changeAlgorithm();
  //  }
   changeAlgorithm(event){
     const target = event.target;
     this.props.changeAlgorithm(target.textContent);
   }
   handleInputs(e){
     const tar = e.target;
     const obj = {};
     obj[tar.id] = tar.value;
     this.props.changeInput(obj);
   }
   handleChecks(e){
     const tar = e.target;
     const obj = {};
     obj[tar.id] = !this.props[tar.id];
     this.props.changeCheck(obj);
   }
   handleInputsDisabled(e){
     const tar = e.target;
     const obj = {};
     obj[tar.id] = {};
     obj[tar.id].value = tar.value;
     obj[tar.id].disabled = false;
     this.props.changeInput(obj);
   }

  render(){
    console.log(this.props);
    return (
      <div>
        <Container style={Formulari}>

          <Form>
            <Row>
            <Col>
              <Slider
                min={3}
                max={20}
                defaultValue={10}
                value={this.props.height}
                onChange={this.heightChanged.bind(this)}/>
            </Col>
            <Col>
            <Slider
              min={3}
              max={20}
              defaultValue={10}
              value={this.props.width}
              onChange={this.widthChanged.bind(this)}/>
            </Col>
            </Row>
            <Row>
            <Col>
            <div style={{ marginTop: "20px" }}>
            <DropdownButton id="dropdown-algorithm" variant='success' title={this.props.alg}>
              <Dropdown.Item key={"DQN"} active={this.props.alg==="DQN" ? true : false}  onClick={this.changeAlgorithm.bind(this)}>DQN</Dropdown.Item>
              <Dropdown.Item key={"GA"} active={this.props.alg==="GA" ? true : false}  onClick={this.changeAlgorithm.bind(this)}>GA</Dropdown.Item>
              <Dropdown.Item key={"RWB"} active={this.props.alg==="RWB" ? true : false}  onClick={this.changeAlgorithm.bind(this)}>RWB</Dropdown.Item>
              <Dropdown.Item key={"A2C"} active={this.props.alg==="A2C" ? true : false}  onClick={this.changeAlgorithm.bind(this)}>A2C</Dropdown.Item>
            </DropdownButton>
            </div>
            </Col>
            <Col>
            <Form.Group controlId="version">
              <Form.Label>Version Name</Form.Label>
              <Form.Control type="text" placeholder="DQN.test.0" onChange={this.handleInputs.bind(this)} value={this.props.version}/>
            </Form.Group>
            </Col>
            </Row>
            <Row>
            <Col>
            <Form.Group controlId="tensorboard">
              <Form.Check type="checkbox" label="Tensorboard" inline="true" onClick={this.handleChecks.bind(this)} checked={this.props.tensorboard}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="done_reward">
              <Form.Label>Done Reward</Form.Label>
              <Form.Control type="text" placeholder="10" onChange={this.handleInputs.bind(this)} value={this.props.done_reward}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="saveweights">
              <Form.Check type="checkbox" label="Save Weights" inline="true" onClick={this.handleChecks.bind(this)} checked={this.props.saveweights}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="edge_value">
              <Form.Label>Edge Value</Form.Label>
              <Form.Control type="text" placeholder="-1" onChange={this.handleInputs.bind(this)} value={this.props.edge_value}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="savefreq">
              <Form.Label>Save Freq.</Form.Label>
              <Form.Control type="text" placeholder="1000" onChange={this.handleInputs.bind(this)} value={this.props.savefreq}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="numAgents">
              <Form.Label>Num. Agents</Form.Label>
              <Form.Control type="text" placeholder="1" onChange={this.handleInputs.bind(this)} value={this.props.numAgents}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="numwalls">
              <Form.Label>Num. Walls</Form.Label>
              <Form.Control type="text" disabled={this.props.numwalls.disabled} onChange={this.handleInputs.bind(this)} placeholder="15" value={this.props.numwalls.value}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="epsmax">
              <Form.Label>Eps. Max</Form.Label>
              <Form.Control type="text" placeholder="0.7" onChange={this.handleInputs.bind(this)} value={this.props.epsmax}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="iterations">
              <Form.Label>Iterations</Form.Label>
              <Form.Control type="text" placeholder="10000" onChange={this.handleInputs.bind(this)} value={this.props.iterations}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="epsmin">
              <Form.Label>Eps. Min</Form.Label>
              <Form.Control type="text" placeholder="0.0001" onChange={this.handleInputs.bind(this)} value={this.props.epsmin}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="health">
              <Form.Label>Health</Form.Label>
              <Form.Control type="text" placeholder="20" onChange={this.handleInputs.bind(this)} value={this.props.health}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="batch_size">
              <Form.Label>Batch Size</Form.Label>
              <Form.Control type="text" disabled={this.props.batch_size.disabled} onChange={this.handleInputsDisabled.bind(this)} placeholder="1000" value={this.props.batch_size.value}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="variance">
              <Form.Label>Variance</Form.Label>
              <Form.Control type="text" disabled={this.props.variance.disabled} onChange={this.handleInputsDisabled.bind(this)} placeholder="0.03" value={this.props.variance.value}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="normal_reward">
              <Form.Label>Norm. Reward</Form.Label>
              <Form.Control type="text" placeholder="-0.04" onChange={this.handleInputs.bind(this)} value={this.props.normal_reward}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="min_wall">
              <Form.Label>Min Wall</Form.Label>
              <Form.Control type="text" placeholder="-1.0" onChange={this.handleInputs.bind(this)} value={this.props.min_wall}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="max_wall">
              <Form.Label>Max Wall</Form.Label>
              <Form.Control type="text" placeholder="0.0" onChange={this.handleInputs.bind(this)} value={this.props.max_wall}/>
            </Form.Group>
            </Col>
            </Row>

            <Row>
            <Col>
            <Form.Group controlId="visibleRad">
              <Form.Label>Visible Rad.</Form.Label>
              <Form.Control type="text" placeholder="1" onChange={this.handleInputs.bind(this)} value={this.props.visibleRad}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="pos">
              <Form.Label>% of selection</Form.Label>
              <Form.Control type="text" disabled={this.props.pos.disabled} onChange={this.handleInputsDisabled.bind(this)} placeholder="0.05" value={this.props.pos.value}/>
            </Form.Group>
            </Col>
            <Col>
            <Form.Group controlId="seed">
              <Form.Label>Seed</Form.Label>
              <Form.Control type="text" placeholder="0" onChange={this.handleInputs.bind(this)} value={this.props.seed}/>
            </Form.Group>
            </Col>
            </Row>
            <Row>
            <Col>
            <Form.Group controlId="po">
              <Form.Check type="checkbox" disabled={this.props.po.disabled} label="Partial Obs." inline="true" onClick={this.handleChecks.bind(this)} checked={this.props.po.value}/>
            </Form.Group>
            </Col>
            </Row>
            <Row>
            <Col>
              <Form.Group controlId="comments">
                <Form.Label>Comments</Form.Label>
                <Form.Control as="textarea" onChange={this.handleInputs.bind(this)} rows="3" value={this.props.comments} />
              </Form.Group>
            </Col>
            </Row>
          </Form>
        </Container>
      </div>
    );
  }
}

const Formulari = {
  width: "100%",
  padding: "30px",
}




const mapStateToProps = ({ formValues }) => {
  const {
    height, width, alg,
    version, tensorboard, saveweights,
    savefreq, iterations, numwalls,
    visibleRad, normal_reward, min_wall,
    max_wall, seed, done_reward,
    edge_value, numAgents,
    epsmax, epsmin, health, batch_size,
    pos, variance, po, comments
    } = formValues;
  return { height, width, alg, version, tensorboard, saveweights,
  savefreq, iterations, numwalls, visibleRad, normal_reward, min_wall,
  max_wall, seed, done_reward, edge_value, numAgents, epsmax, epsmin,
  health, batch_size, pos, variance, po, comments };
};

export default connect(mapStateToProps, {
  heightSlider,
  widthSlider,
  changeAlgorithm,
  changeInput,
  changeCheck
  })(Parameters);
