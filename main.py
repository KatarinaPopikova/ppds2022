import cv2 as cv
import glob

SIZE = 122


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
    imgs1, imgs1_output = load_images('images1')
    imgs2, _ = load_images('images2')


if __name__ == "__main__":
    main()
