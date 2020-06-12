import React from 'react';
import Lobby from './lobby/Lobby.js';
import MainFrame from './components/MainFrame';

class ComponentHandler extends React.Component {

   render() {
      return (
         <div>
            <Lobby/>
         </div>
      );
   }
}

export default ComponentHandler;
