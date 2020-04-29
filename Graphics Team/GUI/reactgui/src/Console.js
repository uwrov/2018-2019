import React, { Component } from 'react';
import './Console.css';


class Console extends Component {
    static thisConsole;
    

    constructor(props) {
        super(props);
        this.prevArgs = []; // list of prev args
        this.argCount = -1;
        this.tempArgNum = 0;
        this.state = { text: '' }//state of the input field 
        this.state = {consoleWindow: ''}//state of the output textbox 
        this.keyPressed = this.keyPressed.bind(this);//event handler for key press
        this.handleChange = this.handleChange.bind(this);//event handler for typing
        this.updateConsole = this.updateConsole.bind(this);//constantly update the console
        this.handleEnter = this.handleEnter.bind(this);//event handler for enter key press
        this.handlePgUp = this.handleBackSlash.bind(this);//even handler for enter key press
        this.addArgs = this.addArgs.bind(this);// add args to array
        this.getPrevArg = this.getPrevArg.bind(this); // get prev arg
        this.consoleStorage = window.localStorage;
        this.data = "Console created.\nListening...\n";
        var temp = "Console created.\nListening...\n";
        this.consoleStorage.setItem('ConsoleData', temp);//set empty console
        let timerId = setInterval(this.updateConsole, 100);//update the console every 100 ms   
    }

    addArgs() {
        if (this.state.text != undefined && this.state.text != "\\") {
            this.prevArgs.push(this.state.text);
            this.argCount += 1; // increment counter
            //console.log(this.argCount);
        }
        
    }
    getPrevArg() {
       
        if (this.tempArgNum >= 0) {
            console.log("This is the arg: " + this.prevArgs[this.tempArgNum]);
            this.setState({
                text: this.prevArgs[this.tempArgNum]
            });
            this.tempArgNum -= 1;
        } else {
            this.setState({
                text: ""
            });
        }
       
        


    }

    updateConsole() {
        try {
            if (this.data == this.consoleStorage.getItem("ConsoleData")) {
                this.setState({ consoleWindow: this.consoleStorage.getItem("ConsoleData") });//update the console every 100 ms
            }
            else {
                this.data = this.consoleStorage.getItem("ConsoleData");
                this.setState({ consoleWindow: this.consoleStorage.getItem("ConsoleData") });
                var textarea = document.getElementById('outputText');
                textarea.scrollTop = textarea.scrollHeight; 

            }
        } catch (e) {
            console.log(e);
       
        }
    }
    handleBackSlash() {
        console.log("triggred");
        this.getPrevArg();
    }
    handleEnter() {
        
        this.addArgs();
        this.tempArgNum = this.argCount; // reset current prev arg to start again
        var temp = this.consoleStorage.getItem('ConsoleData');
        var command = this.state.text + " $";
        var commandArr = Array.from(command);
        if (commandArr[0] == '!') {//command handle
            var commandInfo = command.split(' ');
            if (commandInfo[0] == '!get') {
                if (commandInfo[1] == '$' || commandInfo[1] == '') {//empty string handle
                    temp += "$>" + this.state.text + "\n";
                    temp += "$>" + "no key specified...\n";
                }
                else {
                    temp += "$>" + this.state.text + "\n";
                    temp += "$>" + "the data in " + commandInfo[1] + " is:\n" +
                        this.consoleStorage.getItem(commandInfo[1]) + "\n";
                }
                this.consoleStorage.removeItem('ConsoleData');
                this.consoleStorage.setItem('ConsoleData', temp);
                this.setState({
                    text: "" // clear the input field
                });
                this.setState({
                    consoleWindow: this.consoleStorage.getItem('ConsoleData')
                });


            }
            else {
                temp += "$>" + "command not recognized..." + "\n";
                this.consoleStorage.removeItem('ConsoleData');
                this.consoleStorage.setItem('ConsoleData', temp);
                this.setState({
                    text: "" // clear the input field
                });
                this.setState({
                    consoleWindow: this.consoleStorage.getItem('ConsoleData')
                });

            }
        } else {
            console.log(temp);
            if (this.state.text == undefined) {
                temp += "$>" + "\n";
            }
            else {
                temp += "$>" + this.state.text + "\n";
            }
            console.log(temp);
            this.consoleStorage.removeItem('ConsoleData');
            this.consoleStorage.setItem('ConsoleData', temp);
            this.setState({
                text: "" // clear the input field
            });
            this.setState({
                consoleWindow: this.consoleStorage.getItem('ConsoleData')
            });
        }


    
    }

    handleChange(event) {
        this.setState({ text: event.target.value });
    }

    keyPressed(event) {
        console.log(event.key);
        if (event.key === "Enter") {//if enter is pressed
            event.preventDefault();
            this.handleEnter();
        }
        else if (event.key === "\\") {
            event.preventDefault();
            this.handleBackSlash();
        }
    };
    
        render() {
            return (
                
                <div id="console">
                    < textarea id="outputText" value={this.state.consoleWindow} disabled
                        
                        onChange={this.handleChange.bind(this)}
                        onKeyPress={this.keyPressed.bind(this)}
                        
                        rows="20"
                        cols="106"
                    > </textarea>
                  

                    
                    
                  
                   
                       
                    <textarea id="in" rows="1" cols="106" name = "t" value={this.state.text} 
                        placeholder="your command here"
                        type="text"
                        onChange={this.handleChange.bind(this)}
                        onKeyPress={this.keyPressed.bind(this)}
                        >


                        </textarea>
                        
                        

                </div>

            )
        }
}





export default Console;
