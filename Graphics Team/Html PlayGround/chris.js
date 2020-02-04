/*
*
*/

	"use strict";


	let balance = 100;


	window.addEventListener("load", init);

	/**
    *	Is to be called when the page loads. initiates all the event listener in the starting
    * 	screen
    */
  	function init() {
		document.getElementById("add").addEventListener("click", add);
		document.getElementById("subtract").addEventListener("click", subtract);
		document.getElementById("heads").addEventListener("click", coinFlip);
		document.getElementById("tails").addEventListener("click", coinFlip);
  	}

	function add() {
		let a = document.getElementById("num_a").value;
		let b = document.getElementById("num_b").value;
		a = parseFloat(a);
		b = parseFloat(b);

		document.getElementById("ans").innerText = a + b;

	}

	function subtract() {
		let a = document.getElementById("num_a").value;
		let b = document.getElementById("num_b").value;
		a = parseFloat(a);
		b = parseFloat(b);
		document.getElementById("ans").innerText = a - b;
	}

	function getBet() {
		return document.getElementById("bet-input").value;
	}

	function coinFlip() {
		console.log("Click!");
		let bet = getBet();
		if(bet == null || bet > balance) {
			cantBet();
		} else {
			let guess = this.value;
			let num = Math.floor(Math.random() * 2);
			//heads = 1
			//tails = 0
			let result;
			if(num == 0) {
				result = "tails";
			} else if(num == 1) {
				result = "heads";
			}

			let win = result == guess;
			if(win) {
				balance += parseInt(bet);
				document.getElementById("coin-results").innerText = "You win!";
			} else {
				balance -= parseInt(bet);
				document.getElementById("coin-results").innerText = "You lose!";
			}
			updateBalance();
			document.getElementById("coin-results").innerText += " Flip was " + result +
												", Your guess was " + guess + "!";

		}
	}

	function cantBet() {
		document.getElementById("coin-results").innerText = "You don't have enough money!";
	}

	function updateBalance() {
		document.getElementById("balance").innerText = balance;
	}


	// Gamepad test
	let allGamepads = [];
	// buttons to be changed
	let buttonMappings = [];
	let axisMappings = [];

	let prevTimeStamp = [];

	const BUTTON_NAME = {
		0: "a",			//A
		1: "b",			//B
		2: "x",			//X
		3: "y",			//Y
		4: "lb",			//Left Bumper
		5: "rb",			//Right Bumper
		6: "lt",			//Left Trigger
		7: "rt",			//Right Trigger
		8: "back",		//Back
		9: "start",		//Start
		10: "lstick",		//Left Stick Click
		11: "rstick",		//Right Stick Click
		12: "dup",		//D-pad up
		13: "ddown",		//D-pad down
		14: "dleft",		//D-pad left
		15: "dright",		//D-pad right
		16: "xb"			//Xbox button
	}

	const AXIS = {
		0: "lstick_x",  // Left stick, x axis
		1: "lstick_y",  // Go figure.
		2: "rstick_x",  // Strangely, the pattern repeats.
		3: "rstick_y"
	}

	let listeningToController = false;
	let controllerInterval;


	window.addEventListener("gamepadconnected", function(e) {
		console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
		e.gamepad.index, e.gamepad.id,
		e.gamepad.buttons.length, e.gamepad.axes.length);
		let gamepad = e.gamepad;
		allGamepads[gamepad.index] = gamepad;
		configGamePad(allGamepads[gamepad.index]);

		if(!listeningToController) {
			listeningToController = true;
			controllerInterval = setInterval(updateControls, 10);
		}
	});

	function updateControls() {
		updateGamepadState();
		for(let i = 0; i < allGamepads.length; i++) {
			let currGamepad = allGamepads[i];
			let bMap = buttonMappings[i];
			let aMap = axisMappings[i];
			if(currGamepad.timestamp != prevTimeStamp[i]) {
				for(let j = 0; j < currGamepad.buttons.length; j++) {
					if(currGamepad.buttons[j].pressed !== bMap[j].prevState) {
						if(currGamepad.buttons[j].pressed) {
							bMap[j].func_press(BUTTON_NAME[j]);
						} else {
							bMap[j].func_release(BUTTON_NAME[j]);
						}
						bMap[j].prevState = currGamepad.buttons[j].pressed;
					}
				}
				for(let j = 0; j < currGamepad.axes.length; j++) {
					if(currGamepad.axes[j] !== aMap[j].prevState) {
						console.log(AXIS[j] + ": " + currGamepad.axes[j]);
						aMap[j].prevState = currGamepad.axes[j];
					}
				}
				prevTimeStamp[i] = currGamepad.timestamp;
			}
		}
	}



	function configGamePad(gp) {
		let buttons = [];
		let axes = [];
		gp.buttons.forEach(function() {
			buttons[buttons.length] = {
				prevState: false,
				func_press: function(name) {
					console.log(name + " has been pressed!");
				},
				func_release: function(name) {
					console.log(name + " has been released!");
				}
			};
		});
		gp.axes.forEach(function() {
			axes[axes.length] = {
				prevState: 0.0,
			};
		});
		buttonMappings[gp.index] = buttons;
		axisMappings[gp.index] = axes;
		prevTimeStamp[gp.index] = gp.timestamp;
	}

	function updateGamepadState() {
	  let gamepads = navigator.getGamepads ? navigator.getGamepads() :
	  					(navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);

	  for (var i = 0; i < gamepads.length; i++) {
		  if (gamepads[i]) {
				allGamepads[gamepads[i].index] = gamepads[i];
		  }
	  }
	}
