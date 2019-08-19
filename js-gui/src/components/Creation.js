import React, { Component } from 'react';
import Grid from './Grid';
import Parameters from './Parameters';


class Creation extends Component {



  render(){

    return (
      <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around' }}>
        <Parameters/>
        <Grid
          preview={true}
          height={10}
          width={10}
          walls={[]}
          initstate={[]}
          finalstate={[]}
          />
      </div>
    );
  }
}



export default Creation;
