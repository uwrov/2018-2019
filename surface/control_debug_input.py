from __future__ import print_function
import surface_comm_bottle

from inputs import get_gamepad
import math
import threading


class XboxController():
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self.enable = 1

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def disable(self):
        self.enable = 0

    def enable(self):
        self.enable = 1

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            if(self.enable == 1):
                for event in events:
                    if event.code == 'ABS_Y':
                        surface_comm_bottle.store_state("lstick-y", -event.state / XboxController.MAX_JOY_VAL)
                        self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_X':
                        surface_comm_bottle.store_state("lstick-x", event.state / XboxController.MAX_JOY_VAL)
                        self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RY':
                        surface_comm_bottle.store_state("rstick-y", -event.state / XboxController.MAX_JOY_VAL)
                        self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RX':
                        surface_comm_bottle.store_state("rstick-x", event.state / XboxController.MAX_JOY_VAL)
                        self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_Z':
                        surface_comm_bottle.store_state("ltrigger", event.state /  XboxController.MAX_TRIG_VAL)
                        self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'ABS_RZ':
                        surface_comm_bottle.store_state("rtrigger", event.state /  XboxController.MAX_TRIG_VAL)
                        self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'BTN_TL':
                        surface_comm_bottle.store_state("lb", event.state)
                        self.LeftBumper = event.state
                    elif event.code == 'BTN_TR':
                        surface_comm_bottle.store_state("rb", event.state)
                        self.RightBumper = event.state
                    elif event.code == 'BTN_SOUTH':
                        self.A = event.state
                    elif event.code == 'BTN_NORTH':
                        self.X = event.state
                    elif event.code == 'BTN_WEST':
                        self.Y = event.state
                    elif event.code == 'BTN_EAST':
                        self.B = event.state
                    elif event.code == 'BTN_THUMBL':
                        surface_comm_bottle.store_state("leftstick", event.state)
                        self.LeftThumb = event.state
                    elif event.code == 'BTN_THUMBR':
                        surface_comm_bottle.store_state("rightstick", event.state)
                        self.RightThumb = event.state
                    elif event.code == 'BTN_SELECT':
                        self.Back = event.state
                    elif event.code == 'BTN_START':
                        self.Start = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY1':
                        surface_comm_bottle.store_state("dleft", event.state)
                        self.LeftDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY2':
                        surface_comm_bottle.store_state("dright", event.state)
                        self.RightDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY3':
                        surface_comm_bottle.store_state("dup", event.state)
                        self.UpDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY4':
                        surface_comm_bottle.store_state("ddown", event.state)
                        self.DownDPad = event.state
