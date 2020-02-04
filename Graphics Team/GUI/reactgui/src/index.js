import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import MainCam from "./MainCam";
import * as serviceWorker from './serviceWorker';

let d = new MainCam();

ReactDOM.render(d.render(), document.getElementById("root"));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
