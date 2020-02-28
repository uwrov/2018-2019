import React from 'react';
import "./stylesheets/NavBar.css";
import Button from 'react-bootstrap/Button'
import DropdownButton from 'react-bootstrap/DropdownButton'

class NavBar extends React.Component {


state = {
  buttons: [],

}

  constructor(props) {
    super(props);

    if(this.props.buttons != null) {
      this.state.buttons = this.props.buttons;
    }
    console.log(this.props.buttons)
    console.log(this.state.buttons)
  }





  render() {
    return(
      <div id="NavBar">
        {this.state.buttons.map(button => (
          <Button id={button.text} key={button.id} value={button.value} onClick={button.onClick} >{button.text}</Button>
        ))}






      </div>
    );


    function changeText(buttonIndex, text) {
      this.setState(this.state.buttons[buttonIndex].text , text);
    }
  }



}

export default NavBar;
