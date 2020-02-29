import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Console from './Console.js';
//import App from './App';
import GUI from "./components/GUI.js";
import * as serviceWorker from './serviceWorker';


//ReactDOM.render(<App />, document.getElementById('root'));

//let button = new Button();
ReactDOM.render(<GUI />, document.getElementById('root'));
//ReactDOM.render(button.render(), document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register();
