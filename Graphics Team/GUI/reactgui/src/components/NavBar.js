import React from 'react';
import Button from 'react-bootstrap/Button'
import DropdownButton from 'react-bootstrap/DropdownButton'

class NavBar extends React.Component {


state = {
  buttons: [
    {
      id: 'SettingsButton',
      value: "Settings",
      text: "Settings"
    },
    {
      id: 'DebuggerButton',
      value: "Debugger",
      text: "Debugger"
    },

  ]

}



  render() {
    return(
      <div>
        {this.state.buttons.map(button => (
          <Button key={button.id} value={button.value}>{button.text}</Button>
        ))}

        <DropdownButton> </DropdownButton>




      </div>
    );

    function changeText(buttonIndex, text) {
      this.setState(this.state.buttons[buttonIndex].text , text);
    }
  }



}

export default NavBar;
