import sys, getopt
import numpy as np
import cv2
import argparse
 
def crop(image, width, height):
        image_width = image.shape[0]
        image_height = image.shape[1]
        x = (image_width-width)/2
        y = (image_height-height)/2
        cropped_image = image[x:x+width, y:y+height]
        return cropped_image

def resize(image, height):
	ratio = float(height) / image.shape[1]
        dim = (height, int(image.shape[0] * ratio))
        resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	return resized_image

parser = argparse.ArgumentParser(description='Crop or resize image')
parser.add_argument('-i', '--input')
parser.add_argument('-r', '--resize')
parser.add_argument('-c', '--crop')
args = parser.parse_args()
#print(args.crop)

image = cv2.imread(args.input)
 
if args.crop != None:
	values = args.crop.split(':')
	image = crop(image, int(values[0]), int(values[1]))

if args.resize != None:
	image = resize(image, int(args.resize))

#print(image.shape)

cv2.imshow("Image", image)
#image = crop(image, 375, 375)
#cv2.imshow("Cropped Image", image)
#image = resize(image, 500)
#cv2.imshow("Resized Image", image)
cv2.waitKey(0)
