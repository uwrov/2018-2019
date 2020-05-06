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

		//button listeners for displaying values
		for(let i = 0; i <= 5; i++) {
			addButtonListener(0, i, "pressed", pressedDisplayValue);
			addButtonListener(0, i, "released", releasedDisplayValue);
		}
		for(let i = 8; i <= 16; i++) {
			addButtonListener(0, i, "pressed", pressedDisplayValue);
			addButtonListener(0, i, "released", releasedDisplayValue);
		}
		//addButtonListener(0, 6, "pressed", printValue);
		addButtonListener(0, 6, "released", releasedDisplayValue);
		//addButtonListener(0, 7, "pressed", printValue);
		addButtonListener(0, 7, "released", releasedDisplayValue);

		//button listeners for the functionality
		for(let i = 0; i <= 3; i++) {
			addButtonListener(0, i, "pressed", pressedButton);
			addButtonListener(0, i, "released", releasedButton);
		}
		for(let i = 8; i <= 11; i++) {
			addButtonListener(0, i, "pressed", pressedButton);
			addButtonListener(0, i, "released", releasedButton);
		}
		for(let i = 4; i <= 5; i++) {
			addButtonListener(0, i, "pressed", pressedReveal);
			addButtonListener(0, i, "released", releasedHide);
		}
		for(let i = 12; i <= 15; i++) {
			addButtonListener(0, i, "pressed", pressedReveal);
			addButtonListener(0, i, "released", releasedHide);
		}

		//button listeners for the axis
		addAxisListener(0, 0, updatePos);
		addAxisListener(0, 1, updatePos);
		addAxisListener(0, 2, updatePos);
		addAxisListener(0, 3, updatePos);

	});

	function updateControls() {
		updateGamepadState();
		for(let i = 0; i < allGamepads.length; i++) {
			let currGamepad = allGamepads[i];
			let bMap = buttonMappings[i];
			let aMap = axisMappings[i];
			if(currGamepad.timestamp != prevTimeStamp[i]) {
				for(let j = 0; j < currGamepad.buttons.length; j++) {
					if(currGamepad.buttons[j].value !== bMap[j].prevState) {
						if(currGamepad.buttons[j].pressed) {
							bMap[j].func_press.forEach(function(func) {
								func(BUTTON_NAME[j], currGamepad.buttons[j].value);
							});
						} else {
							bMap[j].func_release.forEach(function(func) {
								func(BUTTON_NAME[j], currGamepad.buttons[j].value);
							});
						}
						bMap[j].prevState = currGamepad.buttons[j].value;
					}
				}
				for(let j = 0; j < currGamepad.axes.length; j++) {
					//if(currGamepad.axes[j] !== aMap[j].prevState) {
						aMap[j].prevState = currGamepad.axes[j];
						aMap[j].func_change.forEach(function(func) {
							func(AXIS[j], currGamepad.axes[j]);
						});
					//}
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
				prevState: 0.0,
				func_press: [
					function(name, value) {
						console.log(name + " has been pressed");
					}
				],
				func_release: [
					function(name) {
						console.log(name + " has been released!");
					}
				]
			};
		});
		gp.axes.forEach(function() {
			axes[axes.length] = {
				prevState: 0.0,
				func_change: [
					function(name, value) {
						console.log(name + ": " + value);
						//document.getElementById(name).innerText = value;
					},
				]
			};
		});
		buttonMappings[gp.index] = buttons;
		axisMappings[gp.index] = axes;
		prevTimeStamp[gp.index] = gp.timestamp;
	}

	function addButtonListener(index, buttonIndex, type, func) {
		if(type ==="pressed") {
			buttonMappings[index][buttonIndex].func_press.push(func);
		} else {
			buttonMappings[index][buttonIndex].func_release.push(func);
		}
	}

	function addAxisListener(index, axisIndex, func) {
		axisMappings[index][axisIndex].func_change.push(func);
	}


	function pressedDisplayValue(name, value) {
		document.getElementById(name+"-image").innerText = "Pressed";

	}
	function releasedDisplayValue(name) {
		document.getElementById(name + "-image").innerText = "Not Pressed";
	}

	function printValue(name, value) {
		console.log(name + " value is " + value);
		document.getElementById(name + "-image").innerText = value;
	}

	function pressedButton(name, value) {
		let element = document.getElementById(name + "-image");
		element.style.filter = "brightness(50%)";
		if(name == "a" || name == "b" || name == "x" || name == "y" || name == "back" || name == "start") {
			let tempP = getComputedStyle(element).top;
			let pixels = parseInt(tempP.replace(/px/,"")) + 5 + "px";
			console.log(pixels);
			element.style.top = pixels;
		}
	}
	function releasedButton(name, value) {
		let element = document.getElementById(name + "-image");
		element.style.filter = "brightness(100%)";
		if(name == "a" || name == "b" || name == "x" || name == "y" || name == "back" || name == "start") {
			let tempP = getComputedStyle(element).top;
			let pixels = parseInt(tempP.replace(/px/,"")) - 5 + "px";
			element.style.top = pixels;
		}
	}
	function pressedReveal(name, value) {
		let element = document.getElementById(name + "-image");
		element.style.visibility = "visible";
	}
	function releasedHide(name, value) {
		let element = document.getElementById(name + "-image");
		element.style.visibility = "hidden";
	}
	function updateDarkness(name, value) {

	}

	function updatePos(name, value) {
		let isX = name == "lstick_x" || name == "rstick_x";
		let stick = (name == "lstick_x" || name == "lstick_y") ? "lstick" : "rstick";
		let element = document.getElementById(stick + "-image");
		let tempP = (isX) ? getComputedStyle(element).left : getComputedStyle(element).top;
		//console.log(name + ": " + tempP);
		//let pixels = parseInt(tempP.replace(/px/,"")) + Math.round(5 * value) + "px";
		//console.log(pixels);
		if(isX) {
			if(stick == "lstick") {
				element.style.left = 89 + 20 * value + "px";
			} else {
				element.style.left = 387 + 20 * value + "px";
			}

		} else {
			if(stick == "lstick") {
				element.style.top = 167 + 20 * value + "px";
			} else {
				element.style.top = 289 + 20 * value + "px";
			}
		}
	}


//////////to change
	function removeButtonListener(index, type, func) {
		if(type ==="pressed") {
			buttonMappings[index][buttonIndex].func_press.remove(func);
		} else {
			buttonMappings[index][buttonIndex].func_release.remove(func);
		}
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
