import React, { Component } from 'react';
import  { Breakpoint, BreakpointProvider } from 'react-socks';
import Grid from './Grid';
import Parameters from './Parameters';


class Creation extends Component {



  render(){

    return (
      <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch', padding: '12px' }}>
        <BreakpointProvider>
          <Breakpoint medium down>
            <div style={{ display:'flex', flexDirection: 'column', justifyContent: 'space-around', alignItems: 'stretch', padding: '5px' }}>
              <Parameters/>
              <Grid
              preview={400}
              height={10}
              width={10}
              walls={[]}
              initstate={[]}
              finalstate={[]}
              />
            </div>
          </Breakpoint>
          <Breakpoint large up>
            <div style={{ display:'flex', flexDirection: 'row', justifyContent: 'space-around', alignItems: 'stretch', padding: '5px' }}>
              <Parameters/>
              <Grid
              preview={700}
              height={10}
              width={10}
              walls={[]}
              initstate={[]}
              finalstate={[]}
              />
            </div>
          </Breakpoint>
        </BreakpointProvider>
      </div>
    );
  }
}



export default Creation;
