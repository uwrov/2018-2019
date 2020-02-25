import React, { Component } from 'react';
import './Console.css';
import Enter from './ConsoleFunctions'
import ReactDOM from 'react-dom';

class Console extends Component {
    static thisConsole;
    static count = 0;
    static getConsole() {
        if (this.thisConsole == undefined) {
            this.thisConsole = new Console();
        }
        return this.thisConsole;
    }

    constructor(props) {
        super(props);
        this.state = { text: '' }//state of the input field 
        this.state = {text1: ''}//state of the output textbox 
        this.keyPressed = this.keyPressed.bind(this);//event handler for enter press
        this.handleChange = this.handleChange.bind(this);//event handler for typing
        sendToConsole = sendToConsole.bind(this);
      //  this.log = this.log.bind(this);//test
        Console.count += 1;
        
    }

   
      log(output) {
        var d = new Date();
        if (this.state.text1 == '') {
            this.setState({
                text1: d.getHours() + ":"
                    + d.getMinutes() + ":"
                    + d.getSeconds() + " $> "
                    + output
                    + "\n"

            });
        }
        else {
            this.setState({
                text1: this.state.text1

                    + '\n'
                    + d.getHours() + ":"
                    + d.getMinutes() + ":"
                    + d.getSeconds() + " $> "
                    + output
            });//add an if later for undefined
        }
        this.setState({
            text: ''
        })

    }


    handleChange(event) {
        this.setState({ text: event.target.value });
    }
    keyPressed(event) {
        var d = new Date();
 
        if (event.key === "Enter") {
            event.preventDefault();
           
            if (this.state.text1 == '') {
               
                this.setState({
                    text1: d.getHours()+":"
                        + d.getMinutes()+":"
                        + d.getSeconds()+ " $> "
                        + this.state.text
                        + "\n"

                }, console.log("d: " + this.state.text1));
            
               
            }
            else {
                this.setState({
                    text1: this.state.text1
                        
                        + '\n'
                            + d.getHours()+":"
                            + d.getMinutes()+":"
                            + d.getSeconds() + " $> "
                            + this.state.text
                });//add an if later for undefined
            }
            this.setState({
                text: ''
            })
           
            
        }
        
    }
    
        render() {
            return (

                <div id="console">
                    <label>Console</label>
                    < textarea id ="outputText" value={this.state.text1} disabled
                        onChange={this.handleChange.bind(this)}
                        onKeyPress={this.keyPressed.bind(this)}
                        
                        rows="20"
                        cols="80"
                    > </textarea>
                    
                    <textarea id = "in" value={this.state.text} 
                        placeholder="your command here"
                        type="text" rows="20"
                        onChange={this.handleChange.bind(this)}
                        onKeyPress={this.keyPressed.bind(this)}
                        >


                    </textarea>

                </div>

            )
        }
}
function sendToConsole(output) {
   

}


//export function sendToConsole(output) { this.log(output);}
export {sendToConsole};
export default Console;
