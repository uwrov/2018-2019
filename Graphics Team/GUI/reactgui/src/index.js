import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import Button from './Button';
import GUI from "./GUI.js";

//ReactDOM.render(<App />, document.getElementById('root'));

//let button = new Button();

//ReactDOM.render(button.render(), document.getElementById('root'));

ReactDOM.render(<GUI />, document.getElementById('root'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
