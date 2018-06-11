# UWROV 2017-2018
### Code and relevant documentation

Under development
- Drive
- Surface
- Sensor


## Note on Component Documentation

The Python server that runs on the Raspberry Pi aboard the ROV is documented at
`surface/README.md`.
Instructions on manually starting the Python server
as well as how to start the entire ROV
may be found at `IGNITION.md`.
Note that the Python server should automatically start upon login to the ROV.

Instructions on how to operate the ROV's cameras as well as how to log into
the ROV are at `camera/Camera_Doc.txt`.  Note that cameras should automatically start upon login to the ROV.

The HTML GUI that runs on the surface system controlling the ROV is documented
at `surface/gui/README.md`.

Documentation for the code running on the Arduino
may be found in the source code.
Additional information may also be found
in its Raspberry Pi communications counterpart
`surface/internal_communication.py`.


## Overview of ROV Subsystems

This is a cursory summary of the robot's subsystems;
certain things may not be covered.
More details may be found in the source code.
**This summary is not a substitute for full electrical schematics.**


### Raspberry Pi

The Raspberry Pi handles camera feeds,
Ethernet communication with the surface system,
and serial communication with the Arduino.
The latter two functions are implemented by
Python code under `surface` in the repository.
The Python code also converts joystick input
from the surface
into motor firing commands sent over the serial line
to the Arduino
while relaying sensor values from the Arduino back up to the surface.
Camera feeds are streamed using MJPEG-Streamer.


### Arduino

The Arduino communicates with ROV hardware.
It directs motors per commands sent by the Pi,
reads sensor values,
and transmits sensor values to the Pi.


### Cameras

There is one camera mounted inside the pressure hull
at the bow
in between the Arduino and Pi.
An external USB camera
may be mounted into the lower nine-pin plug
(labeled B on inside the pressure hull;
do not mistake it for the similarly-labeled four-pin plug used for a motor)
on the backplate;
note that the USB connector from plug B
**inside** the pressure hull
must be plugged into the Pi for this to work.


### Motors

Motors are controlled by the Afro ESCs.
which are in turn controlled by the Arduino.
Details on how to control the motors can be found in the Arduino source code
as well as `surface/internal_communication.py`.
The four T100 thrusters have two blades each and are used for lateral movement.
Each T100 lateral thruster is labeled with a letter A-D
and should be connected to the backplate plug with the matching letter.
The two T200 thrusters have three blades each and are used for vertical movement.

**FIXME:** Document connections for T200 thrusters.

Motor ESCs are wired to digital I/O pins 2-7 on the Arduino.
Arduino digital I/O pins 2-5 control lateral motors.
pins 6 & 7 control vertical motors.
See source code for details.

**FIXME:** Document which pins correspond to which specific motor letters.


### Power

The surface system supplies power at 48 V DC.
This is converted to 12 V DC and 5V DC on a common ground inside the robot
by various converters.

** *Do Not* touch any part of a live power converter with bare hands**
--- you risk blowing out an expensive component and burning yourself.

**FIXME:** 3D-print plastic covers for all GE Critical Power DC power converters
with power converter rating specifications molded into covers.

ESCs are powered by 12 V on various busses.
The fans also draw +12V DC from an ESC bus
but may be grounded on a different bus.
There is a mixed-voltage bus astern of the Arduino
with 5V and 12 V supplies;
even though most of the bus is labeled,
always test voltages before connecting something to it.

Pi and Arduino draw from the 5V portion of the mixed bus.

LED lights and other low-power devices may be powered by a low-voltage bus
somewhere in the bowels of the ROV.

**FIXME:** Consult and update schematics.
