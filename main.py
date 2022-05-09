import numpy
from numba import cuda
from math import ceil
import cv2 as cv
import glob

SIZE = 122


@cuda.jit
def my_kernel(data, data2):
    x, y = cuda.grid(2)
    x_max, y_max = data.shape[:2]
    if x < x_max and y < y_max:
        data[x][y][0] = (int(data[x][y][0]) + int(data2[x][y][0])) / 2
        data[x][y][1] = (int(data[x][y][1]) + int(data2[x][y][1])) / 2
        data[x][y][2] = (int(data[x][y][2]) + int(data2[x][y][2])) / 2


def load_images(path):
    images = glob.glob(path + '/*.jpg')
    imgs = []
    imgs_copy = []
    for img in images:
        original_img = cv.imread(img, 1)
        original_img = cv.resize(original_img, (SIZE, SIZE), interpolation=cv.INTER_AREA)

        imgs.append(original_img)
        imgs_copy.append(original_img.copy())

    return imgs, imgs_copy


def main():
    NUM_ARRAYS = 3
    imgs1, imgs1_output = load_images('images1')
    imgs2, _ = load_images('images2')

    imgs1_output_gpu = []
    img2_gpu = []
    img1_gpu_out = []
    streams = []

    for _ in range(NUM_ARRAYS):
        streams.append(cuda.stream())

    for k in range(NUM_ARRAYS):
        imgs1_output_gpu.append(cuda.to_device(imgs1_output[k], stream=streams[k]))
        img2_gpu.append(cuda.to_device(imgs2[k], stream=streams[k]))

    for k in range(NUM_ARRAYS):
        thread_per_block = (16, 16)
        block_per_grid_x = ceil(imgs1[0].shape[0] / thread_per_block[0])
        block_per_grid_y = ceil(imgs1[0].shape[1] / thread_per_block[1])
        block_per_grid = (block_per_grid_x, block_per_grid_y)

        my_kernel[block_per_grid, thread_per_block, streams[k]](imgs1_output_gpu[k], img2_gpu[k])

    for k in range(NUM_ARRAYS):
        img1_gpu_out.append(imgs1_output_gpu[k].copy_to_host(stream=streams[k]))

    for k in range(NUM_ARRAYS):
        cv.imshow('images' + str(k), numpy.concatenate((imgs1[k], imgs2[k], img1_gpu_out[k]), axis=1))

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
