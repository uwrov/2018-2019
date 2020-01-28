import control_logic
import surface_comm_bottle, control_debug_input
import keyboard
from control_debug_input import XboxController
from tkinter import *

def draw_motor_speed(c, x, y, d_x, d_y, m):
    if (abs(m) >= control_logic.AXIS_CUTOFF):
        MAX_DRAW_DISTANCE = 40
        dist = MAX_DRAW_DISTANCE * m
        if(m < 0):
            fill = "red"
        else:
            fill = "green"
        c.create_line(x, y, d_x * dist + x, d_y * dist + y, fill=fill, arrow=LAST)

def motor_speed(id):
    lateral_motor_speeds = surface_comm_bottle.state_of("lateral_motor_speeds")
    return (lateral_motor_speeds[id] - 128.0) / 128.0

def update_locks(x : IntVar, y : IntVar, z : IntVar):
    surface_comm_bottle.store_state("lock_x", x.get())
    surface_comm_bottle.store_state("lock_y", y.get())
    surface_comm_bottle.store_state("lock_z", z.get())

def draw_cross(c, x, y, color):
    width = 5
    c.create_line(x - width, y - width, x + width + 1, y + width + 1, fill=color)
    c.create_line(x - width, y + width, x + width + 1, y - width - 1, fill=color)

def main():
    top = Tk()
    top.minsize(800, 600)

    centerX = 20
    centerY = 300
    ljoy_label = Label(top, text="Left Joystick")
    ljoy_label.place(x = centerX + 20, y = centerY)
    left_x = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.01, orient= HORIZONTAL)
    left_x.place(x = centerX, y = centerY + 20)
    left_y = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.01)
    left_y.place(x = centerX + 17, y = centerY + 60)

    centerX += 120
    rjoy_label = Label(top, text="Right Joystick")
    rjoy_label.place(x = centerX + 20, y = centerY)
    right_x = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.01, orient= HORIZONTAL)
    right_x.place(x = centerX, y = centerY + 20)
    right_y = Scale(top, from_ = -1.0, to = 1.0, resolution = 0.01)
    right_y.place(x = centerX + 17, y = centerY + 60)

    # Checkboxes for ROV Auto Locks
    centerX += 120
    local_lock_x = IntVar()
    local_lock_y = IntVar()
    local_lock_z = IntVar()

    xLock = Checkbutton(top, text="Auto X Axis", variable=local_lock_x)
    xLock.place( x = centerX, y = centerY)
    yLock = Checkbutton(top, text="Auto Y Axis", variable=local_lock_y)
    yLock.place( x = centerX, y = centerY + 40)
    zLock = Checkbutton(top, text="Auto Z Axis", variable=local_lock_z)
    zLock.place( x = centerX, y = centerY + 80)

    control_logic.AUTO_RUN = 0
    control_logic.DEBUG_MODE = 1
    control_logic.MOTORS_ZEROED = 0
    controller = XboxController()

    while True:
        pass
        if keyboard.is_pressed('q'):
            break

        c = Canvas(top, width = 300, height = 300)
        c.place(x= 0, y = 0)

        # Update and Get ROV Movement
        update_locks(local_lock_x, local_lock_y, local_lock_z)

        left_x.set(surface_comm_bottle.state_of("lstick-x"))
        left_y.set(surface_comm_bottle.state_of("lstick-y"))
        right_x.set(surface_comm_bottle.state_of("rstick-x"))
        right_y.set(surface_comm_bottle.state_of("rstick-y"))
        #surface_comm_bottle.store_state("lstick-x", left_x.get())
        #surface_comm_bottle.store_state("lstick-y", left_y.get())

        #surface_comm_bottle.store_state("rstick-x", right_x.get())
        #surface_comm_bottle.store_state("rstick-y", right_y.get())

        control_logic.compute_and_transmit_motor_states()
        lateral_motor_speeds = surface_comm_bottle.state_of("lateral_motor_speeds")

        # Draw Motor Speeds and ROV Frame
        rov_x = 100
        rov_y = 125
        rov_width = 50 # half of true width
        rov_height = 75 # half of true height

        c.create_rectangle(rov_x - rov_width, rov_y - rov_height, rov_x + rov_width, rov_y + rov_height)

        draw_motor_speed(c, rov_x - rov_width, rov_y - rov_height, 1, -1, (lateral_motor_speeds[0] - 128.0) / 128.0)
        draw_motor_speed(c, rov_x + rov_width, rov_y - rov_height, -1, -1, (lateral_motor_speeds[1] - 128.0) / 128.0)

        draw_motor_speed(c, rov_x - rov_width, rov_y + rov_height, -1, -1, (lateral_motor_speeds[2] - 128.0) / 128.0)
        draw_motor_speed(c, rov_x + rov_width, rov_y + rov_height, 1, -1, (lateral_motor_speeds[3] - 128.0) / 128.0)

        # Draw Net Movement and Rotation Arrows
        net_x = motor_speed(0) - motor_speed(1) - motor_speed(2) + motor_speed(3)
        net_y = -(motor_speed(0) + motor_speed(1) + motor_speed(2) + motor_speed(3))
        net_rotate = motor_speed(0) + motor_speed(2) - (motor_speed(1) + motor_speed(3))
        max_distance = 50

        c.create_line(rov_x, rov_y, rov_x + net_x * max_distance, rov_y + net_y * max_distance, fill="red", arrow=LAST)
        c.create_text(rov_x + net_x * max_distance, rov_y + net_y * max_distance, fill = "red", text = "Net Movement")

        rotate_height = rov_y - rov_height - 25
        c.create_line (rov_x, rotate_height, rov_x + net_rotate * max_distance, rotate_height, fill="blue", arrow=LAST)
        c.create_text(rov_x + net_rotate * max_distance, rotate_height, fill = "blue", text = "Net Rotation")

        mouse_x = top.winfo_pointerx() - top.winfo_rootx()
        mouse_y = top.winfo_pointery() - top.winfo_rooty()
        draw_cross(c, mouse_x, mouse_y, "magenta")

        pixels_per_unit = 5
        target_pos = surface_comm_bottle.state_of("target")
        draw_cross(c, target_pos.x + rov_x, target_pos.y + rov_y, "red")

        top.update()

if __name__ == "__main__":
    main()
