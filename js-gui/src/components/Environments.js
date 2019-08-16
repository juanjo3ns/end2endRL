import React, { Component } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';
import { fetchEnvironments, fetchSingleEnv } from '../actions';



class Environments extends Component {

  componentDidMount() {
    this.props.fetchEnvironments();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.envs.length !== this.props.envs.length) {
      this.props.fetchEnvironments();
    }
  }
  getStyle(listitem){
    const { activenv } = this.props;
    if (activenv.concat(".json") === listitem){
      return { backgroundColor: "#FFCC99"}
    }else{
      return { backgroundColor: "#FFFFFF" }
    }
  }
  loadEnv(e){
    const target = e.target;
    this.props.fetchSingleEnv(target.textContent);
  }

  renderThreed(index){
    if (this.props.threedlist[index]){
      return(
        <div><span style={{ fontSize: "15px", fontWeight: "bold" }}>3D</span></div>
      );
    }
  }
  renderItem(listitem, index){
    return(
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
        <div onClick={this.loadEnv.bind(this)}><span>{listitem}</span></div>
        {this.renderThreed(index)}
      </div>
    );
  }

  render(){
    return (
      <div style={rootView}>
      <ul className="list-group" style={{ overflow: 'auto', height: '600px',  borderRadius: '10px' }}>
         {this.props.envs.map((listitem, index) => (
           <li
            key={listitem}
            className={"list-group-item"}
            style={this.getStyle(listitem)}>
             {this.renderItem(listitem,index)}
           </li>
         ))}
       </ul>
      </div>

    );
  }
}

const rootView = {
  width: "400px",
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start"
}




const mapStateToProps = ({ environments }) => {
  const { envs, activenv, threedlist } = environments;
  return { envs, activenv, threedlist };
};

export default connect(mapStateToProps, { fetchEnvironments, fetchSingleEnv })(Environments);
