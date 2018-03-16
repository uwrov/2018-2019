# Interprets data received from surface GUI and fires motors and arms
# appropriately.

from math import sqrt
from internal_communication import sendMotorSignal, WAIT_TIME, arduinoSetup, queryMotorSpeed
from thread import start_new_thread
from time import clock, sleep
import bottle, surface_comm_bottle
# import Motor_Joystick_X, Motor_Joystick_Y, DPad_X, DPad_Y

# The following are the states of the four lateral motors.
# Each state is an array with values representing the relative speeds of motors
# that will rotate the robot, move it forward, and etc.
# A value of 1 indicates full forward thurst for a motor; -1 indicates
# full reverse thrust.
# Values correspond to motors as follows:
#    [ topleft , topright , bottomleft , bottomright ]

# Robot rotates clockwise
Rotating_State = [1, -1, 1, -1]
# Robot moves straight forward
Forward_State = [1, 1, 1, 1]
Strafe_Right_State = [1, -1, 1, -1]
Strafe_Forward_State = [1, 1, 1, 1]
Strafe_Magnitude = 0.5  # default weight given to strafing


# Adds lists of numbers together.  All lists must be the same length.
def add_lists(*lists):
    list_of_lists = list(lists)
    result = list_of_lists.pop()  # init result with first list
    # loop through all lists and add to result.
    for l in list_of_lists:
        for i in range(len(l)):
            result[i] += l[i]
    return result

# Multiplies a list of numbers by a scalar factor.
def scale_list(lst, factor):
    return map(lambda lst_element: lst_element * factor, lst)

def constrain_value(value, lower_bound, upper_bound):
    # Function returns value if it is within supplied bounds
    # or the bound that it exceeds.  Useful for mapping over lists...
    if lower_bound < value < upper_bound:
        # within bounds --- return value
        return value
    elif value < lower_bound and value < upper_bound:
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

def shift_and_scale_to_motor_byte(flt):
    # converts float to 8-bit motor byte; supplied float is assumed to be
    # w/in -1 to 1.
    return int((flt * 127) + 128)

# Scales list by factor of 128 and adds 128 to it to create a list of motor power bytes
def convert_list_to_motor_bytes (lst):
    return [int(speed + 128) for speed in scale_list(lst, 127)]

# Computes speeds of motors by composing and scaling states for joystick and dpad.
def compute_lateral_motor_composite_state (m_joystick_x, m_joystick_y, strafe_x, strafe_y):  # This ain't terribly functional.
    # Give weight to Rotating_State and Forward_State; add two together.
    # Joystick y must be degated because the controller reports full forward
    # as -1 .
    net_state = add_lists(scale_list(Rotating_State, m_joystick_x),
                          scale_list(Forward_State, -m_joystick_y))
    # Scale net_state to intended strength intended by joystick.
    # Strength is how far the stick is displaced from the center.
    net_state = normalize_list(net_state)
    net_state = scale_list(net_state, sqrt(m_joystick_x**2 + m_joystick_y**2))
    # Add effect of strafing, then normalize and shift to byte-values
    net_state = add_lists(net_state,
                          scale_list(Strafe_Right_State, strafe_x * Strafe_Magnitude),
                          scale_list(Strafe_Forward_State, strafe_y * Strafe_Magnitude))
    return map(lambda x : constrain_value(x, 0, 255),
               convert_list_to_motor_bytes(net_state))

# Computes and transmits motor states to Arduino.
def compute_and_transmit_motor_states():
    while True:
        lateral_motor_speeds = compute_lateral_motor_composite_state(
            surface_comm_bottle.state_of("rstick-x"),
            surface_comm_bottle.state_of("rstick-y"),
            surface_comm_bottle.state_of("dpad-x"),
            surface_comm_bottle.state_of("dpad-y"))
        # Note that the array of numbers is supposed to represent the array index of the motor in the Arduino.  They should somehow be redefined as constants for portability and readability.
        for motor_speed, motor_number in zip(lateral_motor_speeds, [0, 1, 2, 3]):
            sendMotorSignal(motor_number, motor_speed)
        # Vertical motors
        sendMotorSignal(4, int(192 + 63 * surface_comm_bottle.state_of("rtrigger")))
        sendMotorSignal(5, int(192 + 63 * surface_comm_bottle.state_of("rtrigger")))
        sleep(WAIT_TIME)  # delay between successive calls of this function in its own thread

# Init communications
if (arduinoSetup("/dev/ttyACM1") == 0):
    # This expression will start periodically computating and transmitting motor states
    start_new_thread(compute_and_transmit_motor_states, ())
    start_new_thread(lambda : bottle.run(host='localhost', port=8085), ())


# def tester():
#     while 1:
#         print(Lateral)
#         sleep(5)

# start_new_thread(tester, ())
