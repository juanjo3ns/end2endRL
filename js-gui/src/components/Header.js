import React from 'react';
import FirebaseAuth from './FirebaseAuth';


const Header = () => {
    return (
      <div className="ui secondary pointing menu" style={{ padding: '5px', alignItems: 'center' }}>
        <div className="right menu">
          <FirebaseAuth />
        </div>
      </div>
  )
}

export default Header;
