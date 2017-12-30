# Robot Command and Control

This directory is misnamed; it contains files for both the surface system
and the Raspberry Pi communication system.

Most of this code was based on the 2015-2016 and 2014-2015 repositories.
Porting from these repositories to the new robot setup (replacing
BeagleBone with Arduino, etc) is still in early stages, and catastrophic
bugs are guaranteed.  Please avoid sniffing majick smoke.

## Surface System

Directories:
  - gui/

An HTML5 GUI.  Runs on surface computer and takes input from game
controller and computer to control and configure robot.  See
./gui/README.md for details.


## Raspberry Pi

Files:
  - bottle.py                   Python Bottle server implementation
  - internal-communication.py   Communication between components inside the robot
  - surface-comm-bottle.py      Communication between the robot and the surface control system

Primarily a Python Bottle server that routes data between the surface system
and the Arduino, which controls the hardware.

The surface system communicates with the following URLs defined in surface-comm-bottle.py:
  - /sensor                     Request sensor values
  - /motor/<number>/<value>     Set speed of motor <number> to that indicated by <value> --- see source for details on scaling

Data is sent up to the surface via JSON.
