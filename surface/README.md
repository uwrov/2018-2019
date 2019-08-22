# Robot Command and Control

This directory is misnamed; it contains files for both the surface system
and the Raspberry Pi communication system.

Most of this code was based on the 2015-2016 and 2014-2015 repositories.
Porting from these repositories to the new robot setup (replacing
BeagleBone with Arduino, etc) is now in advanced stages, and catastrophic
bugs are less-than-guaranteed.  Please avoid sniffing majick smoke.

## Surface System

Directories:
  - gui/

An HTML5 GUI.  Runs on surface computer and takes input from game
controller and computer to control and configure robot.  See
`gui/README.md` for details.


## Raspberry Pi

Files:
Name | Description
-----|-------------
bottle.py    |    Python Bottle server implementation
internal_communication.py  |   Communication between components inside the robot (Raspberry Pi, Arduino)
surface_comm_bottle.py   |   Communication between the robot and the surface control system (defines server URLs and responses using Bottle server framework)
control_logic.py   |   Converts gamepad commands received at `surface_comm_bottle.py` into motor-firing instructions; sends them to Arduino using functions defined in `internal_communication.py`.

The surface system communicates with the following URLs defined in surface_comm_bottle.py:
URL   |   Functionality
------|---------------------
/sensor  |  Request sensor values
/movement/<axis-or-button>/<value>  |  Set state of joystick <axis-or-button> to <value>.  Values are stored in a dictionary defined in `surface_comm_bottle.py`, which is then accessed by functions in `control_logic.py`.

Data is sent up to the surface via JSON.

The default port for the Bottle server is 8085.
As of 12 May 2018, the default IP address for the Pi
(and thus the Bottle server)
is assumed to be 192.168.8.101.
However, the router may become fickle again
and assign the Pi a different IP address.

Running
```
python -i control_logic.py
```
in the directory `surface` should manually start the Python server
in interactive mode
(under normal circumstances, you should not have to do this
because the ROV automatically starts the Python server upon login).
Refer to `IGNITION.md` for the authoritative details.
