import control_logic
import surface_comm_bottle, control_debug_input
import keyboard
from control_debug_input import XboxController
from tkinter import *

def draw_motor_speed(c, x, y, d_x, d_y, m):
    MAX_DRAW_DISTANCE = 40
    dist = MAX_DRAW_DISTANCE * m
    if(m < 0):
        fill = "red"
    else:
        fill = "green"
    c.create_line(x, y, d_x * dist + x, d_y * dist + y, fill=fill)


def main():
    top = Tk()
    top.minsize(800, 600)

    centerX = 20
    centerY = 300
    ljoy_label = Label(top, text="Left Joystick")
    ljoy_label.place(x = centerX + 20, y = centerY)
    left_x = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.1, orient= HORIZONTAL)
    left_x.place(x = centerX, y = centerY + 20)
    left_y = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.1)
    left_y.place(x = centerX + 17, y = centerY + 60)

    centerX += 120
    rjoy_label = Label(top, text="Right Joystick")
    rjoy_label.place(x = centerX + 20, y = centerY)
    right_x = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.1, orient= HORIZONTAL)
    right_x.place(x = centerX, y = centerY + 20)
    right_y = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.1)
    right_y.place(x = centerX + 17, y = centerY + 60)

    control_logic.AUTO_RUN = 0
    control_logic.DEBUG_MODE = 1
    controller = XboxController()

    while True:
        pass
        if keyboard.is_pressed('q'):
            break
        c = Canvas(top, width = 300, height = 300)
        c.place(x= 0, y = 0)
        c.create_rectangle(50, 50, 150, 200)

        #surface_comm_bottle.store_state("lstick-x", left_x.get())
        #surface_comm_bottle.store_state("lstick-y", left_y.get())

        #surface_comm_bottle.store_state("rstick-x", right_x.get())
        #surface_comm_bottle.store_state("rstick-y", right_y.get())

        control_logic.compute_and_transmit_motor_states()
        lateral_motor_speeds = surface_comm_bottle.state_of("lateral_motor_speeds")
        draw_motor_speed(c, 50, 50, 1, -1, (lateral_motor_speeds[0] - 128.0) / 128.0)
        draw_motor_speed(c, 150, 50, -1, -1, (lateral_motor_speeds[1] - 128.0) / 128.0)

        draw_motor_speed(c, 50, 200, -1, -1, (lateral_motor_speeds[2] - 128.0) / 128.0)
        draw_motor_speed(c, 150, 200, 1, -1, (lateral_motor_speeds[3] - 128.0) / 128.0)


        top.update()

if __name__ == "__main__":
    main()
