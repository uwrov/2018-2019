"""Identifies shapes in a given cell of data

- Take in a cell
- Use CV to identify what kind of shape the image is
  - shapes are either polygons or objects which reach 2 cells
- Return a list of shape identifies (up to you to decide what identifies to use)

"""

import cv2
import pickle


def identify_shapes(row):
    """Identifies the shapes in the row

        Args:
            row: list of images to be analyzed

        Returns:
            A list of strings representing the
            objects located in each cell.
    """
    shape = "empty"
    pass


if __name__ == '__main__':
    # Test driver
    row = []
    with open('list.pkl', 'rb') as f:
        row = pickle.load(f)

    identify_shapes(row)