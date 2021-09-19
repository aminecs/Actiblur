import React, { useState } from 'react';
import desktopImg from './images/desktop.png';
import mapPin from './images/map_pin.png';
import ccImg from './images/cc.png';
import cancelStream from './images/cancel_stream.png';
import shareBtn from './images/share.png';

import './App.css';

function App() {
  const [toggle, setToggle] = useState(false);

  return (
    <div className="App">
        <img src={desktopImg} className="bg" alt="logo" />
        <div className = "pin" onClick = {() => setToggle(!toggle)}>
          <img src = {mapPin} className = "map-pin" alt = "pin"/>
        </div>
        {toggle &&
        <div className = "liveVideo">
          <div className = "stream">
          <img src="http://localhost:5000/video_feed" width="100%"></img>
          </div>
          <div className = "bottomNav">
            <div className = "left">
              <b>User0129 Stream</b>
              <div>Date: 09.19.21</div>
              <div>Live Since: 9:03am</div>
            </div>
            <img src = {ccImg} />
            <img src = {shareBtn}/>
            <div className = "cancelStreamBtn" onClick = {() => setToggle(!toggle)}>
              <img src = {cancelStream}/>
            </div>
          </div>
        </div>}
    </div>
  );
}

export default App;
