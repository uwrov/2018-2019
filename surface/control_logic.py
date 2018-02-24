# Interprets data received from surface GUI and fires motors and arms
# appropriately.

from math import sqrt
from internal_communication import sendMotorSignal
from surface_comm_bottle import Motor_Joystick_X, Motor_Joystick_Y, DPad_X, DPad_Y

# The following are the states of the four lateral motors.
# Each state is an array with values representing the relative speeds of motors
# that will rotate the robot, move it forward, and etc.
# A value of 1 indicates full forward thurst for a motor; -1 indicates
# full reverse thrust.
# Values correspond to motors as follows:
#    [ topleft , topright , bottomleft , bottomright ]

# Robot moves clockwise
Rotating_State = [1, -1, 1, -1]
# Robot moves straight forward
Forward_State = [1, 1, 1, 1]

# FIXME: Certain variables here representing gamepad values need to be imported
# from surface-comm-bottle.py or vice versa.

# Adds lists of numbers together.  All lists must be the same length.
def add_lists(*lists):
    result = lists.pop()  # init result with first list
    # loop through all lists and add to result.
    for l in lists:
        for i in range(0, len(l))
            result[i] += l[i]
    return result

# Multiplies a list of numbers by a scalar factor.
def scale_list(lst, factor):
    return map(lambda lst_element: lst_element * factor, lst)

# Scales a list of numbers so that the list's value of largest magnitude
# becomes 1 (or -1) and that all numbers are scaled relative to that
# largest value.
def normalize_list(lst):
    highest = max(lst)
    lowest = min(lst)           # could be negative
    if highest > abs(lowest):
        return scale_list(lst, highest)
    else:
        return scale_list(lst, -lowest)

# Scales list by factor of 128 and adds 128 to it to create a list of motor power bytes
def shift_and_scale_to_motor_byte (lst):
    [int(speed + 128) for speed in scale_list(lst, 128)]


# Computes speeds of motors by composing and scaling states for joystick and dpad.
def compute_lateral_motor_composite_state (m_joystick_x, m_joystick_y, strafe_x, strafe_y):  # This ain't terribly functional.
    # Give weight to Rotating_State and Forward_State; add two together.
    net_state = add_lists(scale_list(Rotating_State, m_joystick_x),
                          scale_list(Forward_State, m_joystick_y))
    # Scale net_state to intended strength intended by joystick.
    # Strength is how far the stick is displaced from the center.
    net_state = scale_list(net_state, sqrt(m_joystick_x^2 + m_joystick_y^2))
    # Add effect of strafing, then normalize and shift to byte-values
    net_state = add_lists(net_state,
                          scale_list(Strafe_X_State, strafe_x * Strafe_Magnitude),
                          scale_list(Strafe_Y_State, strafe_y * Strafe_Magnitude))
    net_state = normalize_list(net_state)
    return shift_and_scale_to_motor_byte(net_state)


# TODO: Add function to call compute_lateral_motor_composite_state()
# with the proper gamepad values and transmit the proper motor values
# to Arduino.
# Run this to-be-defined function in a seperate thread.

# Computes and transmits motor states to Arduino.
def compute_and_transmit_motor_states():
    lateral_motor_speeds = compute_lateral_motor_composite_state(Motor_Joystick_X, Motor_Joystick_Y, DPad_X, DPad_Y)
    # Note that the array of numbers is supposed to represent the array index of the motor in the Arduino.  They should somehow be redefined as constants for portability and readability.
    for motor_speed, motor_number in zip(lateral_motor_speeds, [0, 1, 2, 3]):
        sendMotorSignal(motor_number, motor_speed)
    # Need to implement up/down motors here.


    
