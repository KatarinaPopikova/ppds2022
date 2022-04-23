"""Author: Katarína Stasová
    License: MIT
    Simulation of programming on GPU using numba framework. Create an average of two images.
"""

import numpy
from numba import cuda
from math import ceil
import cv2 as cv

SIZE = 122  # size for images shape


@cuda.jit
def my_kernel(data, data2):
    """ Create an average of two images and save it to data.
        Simulation calculation on GPU.

    :param data: first image
    :param data2: second image
    """
    x, y = cuda.grid(2)
    x_max, y_max = data.shape[:2]
    if x < x_max and y < y_max:
        data[x][y][0] = (int(data[x][y][0]) + int(data2[x][y][0])) / 2
        data[x][y][1] = (int(data[x][y][1]) + int(data2[x][y][1])) / 2
        data[x][y][2] = (int(data[x][y][2]) + int(data2[x][y][2])) / 2


def main():
    """ Load images, resize them. Define count of threads per blocks, blocks per grid.
        Sends the calculation to the GPU and displays the change due to the calculation.
    """
    original_img = cv.imread(cv.samples.findFile('resources/images/foto.jpg'))
    original_img = cv.resize(original_img, (SIZE, SIZE), interpolation=cv.INTER_AREA)
    img2 = cv.imread(cv.samples.findFile('resources/images/foto (1).jpg'))
    img2 = cv.resize(img2, (SIZE, SIZE), interpolation=cv.INTER_AREA)
    img = original_img.copy()

    thread_per_block = (16, 16)
    block_per_grid_x = ceil(img.shape[0] / thread_per_block[0])
    block_per_grid_y = ceil(img.shape[1] / thread_per_block[1])
    block_per_grid = (block_per_grid_x, block_per_grid_y)

    my_kernel[block_per_grid, thread_per_block](img, img2)

    cv.imshow('images', numpy.concatenate((original_img, img2, img), axis=0))

    # wait to destroying window
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
