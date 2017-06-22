import cv2
import argparse


def pencil(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, (21, 21), 0, 0)
    image_blend = cv2.divide(image_gray, image_blur, scale=256)

    canvas = cv2.imread('background.jpg', cv2.CV_8UC1)
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



parser = argparse.ArgumentParser(description='Apply filters on images')
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('--pencil', action='store_true')
parser.add_argument('--cartoon', action='store_true')
args = parser.parse_args()
print(args)

image = cv2.imread(args.input)
cv2.imshow("Original", image)

if args.pencil:
    image = pencil(image)

if args.cartoon:
    image = cartoon(image)

if args.output != None:
    cv2.imwrite(args.output, image)

cv2.imshow("Image", image)
cv2.waitKey(0)
