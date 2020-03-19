import detect_angle
import control_line
from track_grid import find_row
from process_cells import process_row
import cv2

# Hi! This script will complete task 2.1 - currently under construction


def main():
    src = 0
    cam = cv2.VideoCapture(src)
    rows = []

    # run video until we have gathered all rows
    while(True):
        ret, frame = cam.read()

        # ====== Ensure that ROV is on track =====
        # detect angle (frame)
        # control line (frame)

        # ====== Collect image data =====
        rows.append(find_row(frame))

        # ====== Management =====
        if cv2.waitKey(27) == 1 or len(rows) == 9:
            return rows

    # ===== Shape Recognition and Finding Results =====
    processed_rows = []
    for row in rows:
        # split each row into cells
        cells = process_row(row)

        # identify the objects in each cell
        # row_contents = identify(cells) (type list)

        # processed_rows.append(row_contents)

    # ===== Graph results =====
    # render_result(processed_rows)

    # === Free resources ===
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
