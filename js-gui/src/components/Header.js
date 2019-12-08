import React from 'react';
import FirebaseAuth from './FirebaseAuth';
import insight from '../img/insight_logo.png';
import sfi from '../img/sfi_logo.png';
import Image from 'react-image-resizer';



const Header = () => {
    return (
      <div className="ui secondary pointing menu" style={{ padding: '5px', alignItems: 'center' }}>
        <div className="center menu" style={{ paddingLeft: "10px", display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center' }}>
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
        <div className="right menu">
          <FirebaseAuth />
        </div>
      </div>
  )
}

export default Header;
