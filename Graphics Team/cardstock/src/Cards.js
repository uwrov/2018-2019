import React from 'react';



class Cards extends Component {
    constructor(props) {
        this.state = { consoleWindow: '' }//state of the output textbox 
        setTimeout(requestCards, 1000);
    }
    requestCards() {
        fetch('https://api.npms.io/v2/search?q=react')
            .then(response => response.json())
            .then(data => this.setState({ consoleWindow: data.total }));
    }
    render() {
        return (
            <div id="console">
                < textarea id="outputText" value={this.state.consoleWindow} disabled
                    rows="20"
                    cols="106"
                > </textarea>
                
            </div>
        )
    }
}

export default App;
