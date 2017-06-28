import cv2
import argparse
import numpy as np


def pencil(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, (21, 21), 0, 0)
    image_blend = cv2.divide(image_gray, image_blur, scale=256)

    canvas = cv2.imread('img/background.jpg', cv2.CV_8UC1)
    canvas = cv2.resize(canvas, (image.shape[1], image.shape[0]))
    image_blend = cv2.multiply(image_blend, canvas, scale=1./256)
    return cv2.cvtColor(image_blend, cv2.COLOR_GRAY2RGB)


def cartoon(image):
    numDownSamples = 2
    numBilateralFilters = 7

    image_color = image
    for _ in xrange(numDownSamples):
        image_color = cv2.pyrDown(image_color)

    for _ in xrange(numBilateralFilters):
        image_color = cv2.bilateralFilter(image_color, 9, 9, 7)

    for _ in xrange(numDownSamples):
        image_color = cv2.pyrUp(image_color)

    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_blur = cv2.medianBlur(image_gray, 7)
    image_edge = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    image_edge = cv2.cvtColor(image_edge, cv2.COLOR_GRAY2RGB)
    return cv2.bitwise_and(image_color, image_edge)


def darker(image):
    kernel_x = cv2.getGaussianKernel(image.shape[1], 200)
    kernel_y = cv2.getGaussianKernel(image.shape[0], 200)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    output = np.copy(image)

    for i in range(3):
        output[:, :, i] = output[:, :, i] * mask

    return output


def sepia(image):
    image_sepia = image
    for x in xrange(image.shape[0]):
        for y in xrange(image.shape[1]):
            R = image[x, y, 2] * 0.393 + image[x, y, 1] * 0.769 + image[x, y, 0] * 0.189
            G = image[x, y, 2] * 0.349 + image[x, y, 1] * 0.686 + image[x, y, 0] * 0.168
            B = image[x, y, 2] * 0.272 + image[x, y, 1] * 0.534 + image[x, y, 0] * 0.131
            if R > 255:
                image_sepia[x, y, 2] = 255
            else:
                image_sepia[x, y, 2] = R
            if G > 255:
                image_sepia[x, y, 1] = 255
            else:
                image_sepia[x, y, 1] = G
            if B > 255:
                image_sepia[x, y, 0] = 255
            else:
                image_sepia[x, y, 0] = B
    return image_sepia


def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thermic(image):
    image_thermic = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(image_thermic)
    return h



parser = argparse.ArgumentParser(description='Apply filters on images')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('--pencil', action='store_true')
parser.add_argument('--cartoon', action='store_true')
parser.add_argument('--darker', action='store_true')
parser.add_argument('--sepia', action='store_true')
parser.add_argument('--gray', action='store_true')
parser.add_argument('--thermic', action='store_true')
args = parser.parse_args()
print(args)

image = cv2.imread(args.input)

if args.pencil:
    image = pencil(image)

if args.cartoon:
    image = cartoon(image)

if args.darker:
    image = darker(image)

if args.sepia:
    image = sepia(image)

if args.gray:
    image = gray(image)

if args.thermic:
    image = thermic(image)

if args.output is not None:
    cv2.imwrite(args.output, image)
