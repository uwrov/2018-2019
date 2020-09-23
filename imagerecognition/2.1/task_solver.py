"""Executable script which performs task 2.1

Currently under construction

Here's what this script should do:
    - Get a camera stream running
    - Spin thread for control systems (control_angle control_height)
    - Spin thread for mapping (track_grid)
    - Kill control systems thread after mapping thread is done
    - Do visualization process
"""

from control_angle import course_correct
import control_height
from track_grid import find_row
from process_row import process_row
import cv2


def main():
    src = 0
    cam = cv2.VideoCapture(src) # consider putting this in its own thread
    rows = []

    # run video until we have gathered all rows
    while(True):
        _, frame = cam.read()

        # ====== Ensure that ROV is on track =====
        # TODO: Consider spinning new thread to do this in background
        course_correct(frame, 10)
        # control line (frame)

        # ====== Collect image data =====
        rows.append(find_row(frame))

        # ====== Management =====
        if cv2.waitKey(27) == 1 or len(rows) == 9:
            return rows

    # ===== Shape Recognition and Finding Results =====
    # processed_rows = []
    # for row in rows:
        # # split each row into cells
        # cells = process_row(row)

        # # identify the objects in each cell
        # row_contents = identify(cells) (type list)

        # processed_rows.append(row_contents)

    # ===== Graph results =====
    # render_result(processed_rows)

    # === Free resources ===
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
