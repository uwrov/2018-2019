import React, { Component } from 'react';
import './Console.css';
import Enter from './ConsoleFunctions'
import ReactDOM from 'react-dom';
//Access - Control - Allow - Origin: *
//Access - Control - Allow - Origin: http://localhost:4000

class Console extends Component {
    static thisConsole;
    

    constructor(props) {
        super(props);
        this.argCounter = 0;
        this.serverText = "";
        this.state = { text: '' }//state of the input field 
        this.state = {text1: ''}//state of the output textbox 
        this.keyPressed = this.keyPressed.bind(this);//event handler for enter press
        this.handleChange = this.handleChange.bind(this);//event handler for typing
        this.clear = this.clear.bind(this);
       // this.t = this.t.bind(this);
        //this.sendToConsole = sendToConsole.bind(this);
      //  this.log = this.log.bind(this);//test
        Console.count += 1;
        let timerId = setInterval(this.clear, 20000);
       
       
        
    }
    
    
    clear() {

        fetch("http://localhost:4000/getOutput")
            .then(this.checkResponse)
            .then((response) => this.setState({ text1: response }))
            .catch(this.handleError);

       
    }
    handleError()
    {

    }
    checkResponse(response) {
        if (!response.ok) {
            throw Error("err");
        }
        return response.text();
    }

    handleChange(event) {
        this.setState({ text: event.target.value });
    }

    keyPressed(event) {
        var d = new Date();
 
        if (event.key === "Enter") {
           event.preventDefault();
           document.getElementById("s").click();  
           this.setState({
                text: ""
           });
            
        }
        
        
    };
    
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
                  

                    <iframe name='t' src='localhost:3000' width="0" height="0" tabindex="-1" title="empty" class="hidden"/>
                    
                  
                    <form id="console" action="http://localhost:4000/console" method="post" target="t">
                       
                        <textarea id="in" width="200" height="20" name = "t" value={this.state.text} 
                        placeholder="your command here"
                        type="text" rows="20"
                        onChange={this.handleChange.bind(this)}
                        onKeyPress={this.keyPressed.bind(this)}
                        >


                        </textarea>
                        <input id="s" type="submit" width="0" height="0" tabindex="-1" title="empty" class="hidden" />
                        </form>

                </div>

            )
        }
}





export default Console;
