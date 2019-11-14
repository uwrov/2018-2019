# Interprets data received from surface GUI and fires motors appropriately.

from math import sqrt
from internal_communication import sendMotorSignal, WAIT_TIME, arduinoSetup, queryMotorSpeed, toggleLED, sendPing, zero_all_motors
from _thread import start_new_thread
from time import clock, sleep
from surface_comm_bottle import position, acceleration, velocity, auto_mode, Vector3
import bottle, surface_comm_bottle, sys, socket, psutil, os

# The following are states for the four lateral motors.
# Each state is an array with values representing the relative speeds of motors
# that will rotate the robot, move it forward, and etc.
# A value of 1 indicates full forward thurst for a motor; -1 indicates
# full reverse thrust.
# Values correspond to motors as follows:
#    [ topleft , topright , bottomleft , bottomright ]

# Robot rotates clockwise
Rotating_State = [1, -1, 1, -1]
# Robot moves straight forward
Strafe_Left_State = [-1, 1, 1, -1]
Strafe_Forward_State = [1, 1, 1, 1]
Strafe_Magnitude = 0.5  # default weight given to strafing

COARSE_SPEED = 127
MEDIUM_SPEED = 60
FINE_SPEED = 20

DEBUG_MODE = 0
AUTO_RUN = 1
MOTORS_ZEROED = 0

AXIS_CUTOFF = 0.05

# When the robot operator tells the robot to move,
# this program will take linear combinations of the above states
# to compute what speeds to run the motors at
# in order to move the robot in the instructed fashion.
# For example, if the operator were pushing the right gamepad stick forward and slightly to the left,
# he or she would be telling the robot to move forward while turning left (ccw).
# This program would see that the joystick is displaced, say, X units on the x-axis and Y units on the y-axis.
# This programs knows that the gamepad stick's x-axis corresopnds to rotation,
# while the y-axis coresponds to forward/backward movement.
# The program would therefore calculate the following (pseudo-code) using the states defined above:
#
#   X*Rotating_State + Y*Forward_State
#
# The program then scales the resulting vector such that its largest element has a magnitude of 1.
# Then the program multiplies the vector by sqrt(X^2+Y^2)
# so that the gamepad stick's displacement from center controls the overall speed of the actual movement
# (the more you displace the gamepad stick, the faster the robot goes).
# It then scales and shifts the vector so that its values lie in between 0 to 255, the acceptable range of a motor byte
# used to communicate with the Arduino (see internal_communication.py and arduino/motor-code/motor-code.ino for details).
# Finally, it transmits the just-computed motor bytes using the functions defined in internal_communication.py
# to the Arduino, which actuates the motors.

def joystick_updated_p():
    return surface_comm_bottle.state_of("update-required")

def reset_joystick_updated():
    surface_comm_bottle.store_state("update-required", False)

# Adds lists of numbers together.  All lists must be the same length.
def add_lists(*lists):
    list_of_lists = list(lists)
    result = list_of_lists.pop()  # init result with first list
    # loop through all remaining lists and add to result.
    for l in list_of_lists:
        for i in range(len(l)):
            result[i] += l[i]
    return result

# Multiplies a list of numbers by a scalar factor.
def scale_list(lst, factor):
    return list(map(lambda lst_element: lst_element * factor, lst))

def constrain_value(value, lower_bound, upper_bound):
    # Function returns value if it is within supplied bounds
    # or the bound that it exceeds.  Useful for mapping over lists...
    if lower_bound < value < upper_bound:
        # within bounds --- return value
        return value
    elif value < lower_bound: #and value < upper_bound:
        # too low --- return lower bound
        return lower_bound
    else:
        # Process of elimination: value must be higher than bound
        return upper_bound

# Scales a list of numbers so that the list's value of largest magnitude
# becomes 1 (or -1) and that all numbers are scaled relative to that
# largest value.
def normalize_list(lst):
    highest = max(lst)
    lowest = min(lst)           # could be negative
    if highest == 0 and lowest == 0:
        return lst
    elif highest >= abs(lowest):
        return scale_list(lst, highest**(-1))
    else:
        return scale_list(lst, (-lowest)**(-1))

# Appears to currently be unused.
def shift_and_scale_to_motor_byte(flt):
    # converts float to 8-bit motor byte; supplied float is assumed to be
    # w/in -1 to 1.
    return int((flt * get_speed_mode()) + 128)

# Scales list by factor of 128 and adds 128 to it to create a list of motor power bytes
def convert_list_to_motor_bytes (lst):
    return [int(speed + 128) for speed in scale_list(lst, get_speed_mode())]

# Returns the current speed coefficient (RT is fine, LT is coarse, neither is medium).
# Coefficients can be modified at the top of the program.
def get_speed_mode():
    if surface_comm_bottle.state_of("rtrigger") == 1:
        return FINE_SPEED;
    elif surface_comm_bottle.state_of("ltrigger") == 1:
        return COARSE_SPEED;
    return MEDIUM_SPEED;

# Computes speeds of motors by composing and scaling states for joystick and dpad.
def compute_lateral_motor_composite_state (m_joystick_x, m_joystick_y, strafe_x, strafe_y):  # This ain't terribly functional.
    # Give weight to Rotating_State and Forward_State; add two together.
    # Joystick y must be negated beforehand because the controller reports full forward
    # as -1 .
    net_state = add_lists(scale_list(Rotating_State, m_joystick_x),
                          scale_list(Strafe_Forward_State, m_joystick_y))
    # Scale net_state to intended strength intended by joystick.
    # Strength is how far the stick is displaced from the center.
    net_state = normalize_list(net_state)
    net_state = scale_list(net_state, sqrt(m_joystick_x**2 + m_joystick_y**2))

    strafe_state = add_lists(scale_list(Strafe_Left_State, strafe_x), scale_list(Strafe_Forward_State, strafe_y))
    strafe_state = normalize_list(strafe_state)
    strafe_state = scale_list(strafe_state, sqrt(strafe_x**2 + strafe_y**2))

    # Add effect of strafing, then normalize and shift to byte-values
    net_state = add_lists(net_state, strafe_state)
    ret = list(map(lambda x : constrain_value(x, 0, 255),
               convert_list_to_motor_bytes(net_state)))
    return ret

# Smooths between a and b by some x (0-1).
def smoothstep(a, b, x):
    x = clamp(x, a, b)
    return x * x * (3 - 2 * x)

# Clamps x to be within the bounds given by min and max.
def clamp(x, min, max):
    if x > max:
        return min
    elif x < max:
        return max
    else:
        return x

# Returns a Vector3 with the speed intensity for the X, Y, and Z movement to reach
# target location.
# [0-1] for each axis.
def moveToTarget() -> Vector3:
    #determine displacement
    xDelta = 0.0
    yDelta = 0.0
    zDelta = 0.0
    if surface_comm_bottle.lockX: #this is inverted, because +x should move in the left direction
        xDelta = position.x - target.x
    if surface_comm_bottle.lockY:
        yDelta = target.y - position.y
    if surface_comm_bottle.lockZ:
        yDelta = target.z - position.z

    displacement = sqrt(xDelta*xDelta + yDelta*yDelta + zDelta*zDelta)
    minimum_speed = 0.0
    maximum_speed = 1.0 #spoof controller input by constraining [0, 1]
    max_speed_distance = 16.0
    speed = smoothstep((displacement / max_speed_distance), minimum_speed, maximum_speed)

    #normalize
    direction = Vector3(xDelta, yDelta, zDelta).normalize()

    return direction * speed;

# Computes and transmits motor states to Arduino.
def compute_and_transmit_motor_states():
    if auto_mode == 1:
        #initiate auto
        var = 0 #so that if branch works correctly
    else:
        if surface_comm_bottle.state_of("leftstick") != 0:
            if MOTORS_ZEROED == 0:
                MOTORS_ZEROED = 1;
                if DEBUG_MODE == 0:
                    zero_all_motors();
        elif joystick_updated_p():  # only compute and transmit if state has changed
            MOTORS_ZEROED = 0;
            reset_joystick_updated()
            #Calculate motor speed
            strafe_x_in = surface_comm_bottle.state_of("dleft") - surface_comm_bottle.state_of("dright") # Calculate strafe_x and strafe_y
            strafe_y_in = surface_comm_bottle.state_of("dup") - surface_comm_bottle.state_of("ddown")
            # Reads joystick if D-Pad has no input (or negates itself)
            if strafe_x_in == 0 and strafe_y_in == 0:
                strafe_x_in = -surface_comm_bottle.state_of("lstick-x")
                strafe_y_in = -surface_comm_bottle.state_of("lstick-y")

            strafe_z_in = surface_comm_bottle.state_of("rtrigger") - surface_comm_bottle.state_of("ltrigger")

            auto_input = moveToTarget()
            if abs(strafe_x_in) < AXIS_CUTOFF:
                strafe_x_in = auto_input.x
            if abs(strafe_y_in) < AXIS_CUTOFF:
                strafe_y_in = auto_input.y
            if abs(strafe_z_in) < AXIS_CUTOFF:
                strafe_z_in = auto_input.z

            lateral_motor_speeds = compute_lateral_motor_composite_state(
                    surface_comm_bottle.state_of("rstick-x"),
                    -surface_comm_bottle.state_of("rstick-y"),
                    strafe_x_in,
                    strafe_y_in)
            vert_motor_byte = int(128 + get_speed_mode() * strafe_z_in)

            surface_comm_bottle.store_state("lateral_motor_speeds", lateral_motor_speeds)
            surface_comm_bottle.store_state("vert_motor_byte", vert_motor_byte)

            if (DEBUG_MODE == 0):
                # Note that the array of numbers is supposed to represent the array index of the motor in the Arduino.  They should somehow be redefined as constants for portability and readability.
                for motor_speed, motor_number in zip(lateral_motor_speeds, [0, 1, 2, 3]):
                    sendMotorSignal(motor_number, motor_speed)
                # Vertical motors --- right gamepad bumper pushes robot down; left one pushes robot up.
                sendMotorSignal(4, vert_motor_byte)
                sendMotorSignal(5, vert_motor_byte)
        sleep(WAIT_TIME)  # delay between successive calls of this function in its own thread

def main_loop():
    while AUTO_RUN == 1:
        compute_and_transmit_motor_states()

# Shell command, zeroes the motors and exits the program.
def kill():
    z()
    quit()

def initiate_communications():
    # Start the Bottle server to receive communications from surface
    max_attempts = 5
    attempts = 5
    while (attempts >= 0):
        try:
            #start_new_thread(lambda : bottle.run(host='192.168.8.102', port=8085), ())
            bottle.run(host='192.168.8.102', port=8085)
            print("[Connected successfully.]")
            break
        except socket.error as serr:
            print(serr)
            print("[Error encountered. Attempt to kill processes and reconnect... ({}/{})]".format(attempts, max_attempts))
            PROCNAME = "python"
            myPID = psutil.Process(os.getpid()).pid
            print(myPID)
            for proc in psutil.process_iter():
                if PROCNAME in proc.name():
                    if myPID != proc.pid:
                        print("Attempting kill on {}, {}".format(proc.name(), proc.pid))
                        proc.kill()
        attempts = attempts - 1

def main():
    # Init communications
    #if (arduinoSetup("/dev/ttyACM0") == 0): #This original statement was to prevent running if arduino not connected
    if (len(sys.argv) > 1):
        # IMPORTANT NOTE! PASSING IN AN ARG WILL AUTOMATICALLY SET
        # THE ROV TO TESTING MODE.
        print("STARTED IN DEBUG MODE: Run without arguments to disable.")
        DEBUG_MODE = 1
        AUTO_RUN = 0
    else:
        print("STARTED IN OP MODE: (Run with arguments to enable debug mode.)")
    print("Type kill() at any time to exit ROV operation safely.")
    # This expression will start periodically computating and transmitting motor states
    initiate_communications()
    main_loop()

if __name__ == "__main__":
    main()
