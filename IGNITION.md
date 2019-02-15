# Starting the ROV

> 1. Find key.
> 1. Insert key into ignition.
> 1. Pump accelerator pedal thrice.
> 1. Turn key.  ROV should now start.
> _Note: avoid flooding the carburetor._

_Last Updated: 2/14/19 by Peyton Lee and Camila Kang

Basic procedure:
1. Wire everything up and power on the robot.
1. Find ROV IP address
1. Log in via Secure Shell (SSH)
1. Start Python server.
1. Start web interface

## Power on robot

1. Connect motors A-D to the corresponding lettered plugs on the ROV's
   backplate.  The backplate plugs have lettered labels on the wires leading up
   to them inside the pressure hull.  Connect the two vertical motors (the ones
   with the one-inch diameter plugs) to the two corresponding _lower_ plugs
   on the backplate.  **Do not use the yellow one-inch plug near the top of
   the backplate.**
1. Screw the tether's power cord into black power box with white switch.
   Plug other end of cord into red ROV plug on backplate.
1. Plug Ethernet cable/tether into eight-pin plug A (the upper eight-pin plug)
   on ROV backplate.  Plug other end into router.
1. Plug router into 120V mains.
1. Plug 48V power converter into mains.  The power converter is the
   silvery-metal box the size of a long brick connected to the black power
   box with the white switch.
1. Turn the white switch on the black power box on.
   This supplies power to the ROV.  Should anything untoward happen to the ROV
   (motors spin up with awful screeching noise, fire breaks out, etc)
   or its operators, immediately turn the white switch off and take the
   appropriate remedial action.
   There is fire extinguisher by the door of the lab.


## Find ROV IP Address

See Step 1 ("Find the ip address of pi") in the file "camera/Camera_Doc.txt"
for instructions on how to determine which IP address the router has assigned
to the Raspberry Pi aboard the ROV.


## Log in via Secure Shell (SSH)

Users of Microsoft Windows NT-derived operating systems should refer to Step 2
("Log into pi") in the file "camera/Camera_Doc.txt" for instructions on how to
log into the Pi via SSH.

_
Step 2: Log into pi
1. Enter pi's ip address (192.168.8.102) to Putty's "Host Name" section; leave
   the "Port" to "22"
   
2. Open a new session; a terminal of pi should pop up

3. Login with user "pi" and password "raspberry"_

Users of Unix-like operating systems may log into the Pi by entering the
following at the command line:
```
ssh pi@192.168.8.102
```
Replace the IP address following the "pi@" with the IP address assigned by the
router to the Pi.  Enter password when prompted.

_Note: Due to a closed-source incompatibility with Microsoft's implementation
of gamepad drivers, users of NT-derived operating systems will not have full
control or functionality of the ROV.  It is recommended that one use a
Unix-like operating system on the surface system connected to the gamepad._


## Start Python server

**Please be advised:** The following section has been automated by placing the
commands indicated below in the file `~/.bashrc`.  The Python server should
start up automagically in interactive mode upon login to the Pi.  No attempt
is made to determine the correct IP address; it is assumed that the router has
assigned the Pi to `192.168.8.102`.  If this has changed, then you ***should***
follow the instructions below to manually configure the IP address and start
the server.  Note also that in `~/.bashrc`, the permissions of `/dev/ttyACM0`
are not set using `chmod`.

This is a pain.

Once you have logged into the Pi, enter the following at the Pi's console:
```
cd 2017-2018/surface
```

Open the file "surface/control_logic.py" in your favorite editor.  If you do
not have a favorite editor, `nano` will get the job done:
```
nano control_logic.py
```
_(You must be in the directory "2017-2018/surface" for the above to work.)_
Find the line resembling
```python
    start_new_thread(lambda : bottle.run(host='192.168.8.101', port=8085), ())
```
(it is very near the end of the file).
Replace the IP address (the `host=` argument) with the IP address of the Pi
as needed.  Save the file and exit the editor.

Run the following at the Pi's console:
```
python -i control_logic.py
```
Python should now start up, start the web server in a separate thread, and enter
interactive mode.  If you hit the return key, you should get a prompt (`>>> `).
Typing Control-C will interrupt any command that takes too long to execute;
Control-D or `exit()` will stop Python and return you the the Raspberry Pi's
command line. 

**USE THE COMMAND kill() TO ZERO MOTORS AND EXIT SAFELY**

_Note: To run the ROV in debug mode, add any argument to the end of the run statement._
```
python -i control_logic.py 0
```

**TODO:** Store Pi's IP address in an environment variable to avoid having to
edit "control_logic.py".
**TODO:** Move ~/.bashrc commands to a different file that executes only upon login, not upon starting a new shell.

**[TROUBLESHOOTING:]

**If** Python complains about not having permission to open `/dev/ttyACM0`,
run the following in the Pi's console to obtain access to `/dev/ttyACM0`
(the serial device that the Pi uses to communicate with the Arduino):
```
sudo chmod 666 /dev/ttyACM0
```
If `/dev/ttyACM0` does not exist, try `/dev/ttyACM1`.  If this occurs,
you will also have to replace the former with the latter in the file
"surface/control_logic.py" similar to the instructions above)_

**If** Python gives the following:
```
socket.error: [Errno 98] Address already in use
```
1. Exit Python using CTRL+D.
2. Type the following command to search for instances of python currently running:
```
ps -fA | grep python
```
3. Locate the process ID number (the second column, usually to the right of the key 'pi') 
for any existing instance of control_logic.py.
4. LEAVE NO SURVIVORS. Type in the following command to kill the process.
```
kill PROCESS_ID
```
5. Repeat step 5 to ensure there are no survivors.
6. If the process(es) is still running, force their death by adding the following directive.
```
kill -9 PROCESS_ID
```
7. Revel in destruction.

## Start web interface

Leave the Raspberry Pi's console alone for a bit.  On the surface system,
open the file "surface/gui/rov-interface.js" in your favorite editor.  Find
the definition for the function `maybe_transmit_axis_value()`.  There should
be a URL (string) bound to the variable `url`.  Change the IP address to the
one corresponding to the Pi if needed.  Save file and exit editor.

**AT THIS POINT, _you must put the ROV into the water if you have not already
done so._**
_You are about to commence communications between the surface controller and
the ROV and risk accidentally turning the motors on.  The motors will break
if run outside of the water._  It should also go without saying that no fingers
should be near the motors.

Open the file "surface/gui/index.html" in Mozilla Firefox.  Plug a gamepad
into the surface system.  If desired, click the gray stripe in the bottom-center
of the page; it should open a pane with progress-bars and readouts that indicate
what buttons and sticks you are pushing on the gamepad.

Connect to the cameras by changing the IP address in the interface menu (upper
gray bar) to the address of the Pi, usually 192.168.8.102.

If you look over at the Raspberry Pi's console, you should now see text logging
received gamepad input if you push a button or stick on the gamepad.  The ROV
should respond accordingly.


LocalWords:  backplate ROV IP gamepad Arduino sudo chmod cd nano py
LocalWords:  TODO url
