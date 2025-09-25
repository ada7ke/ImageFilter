# Version #02 - Added track slider
# Convert an image into grayscale, then convert to 3 colors

# imports
import cv2
import os.path
import eyw

# get image file
print ("Save your original image in the same folder as this program.")
filename_valid = False
while filename_valid == False:
    filename = input("Enter the name of your file, including the "\
                                 "extension, and then press 'enter': ")
    if os.path.isfile(filename) == True:
        filename_valid = True
    else:
        print ("Something was wrong with that filename. Please try again.")

original_image = cv2.imread(filename,1)
grayscale_image_simple = cv2.imread(filename, 0)
grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

# create image windows
cv2.namedWindow('Original Image')
cv2.namedWindow('Grayscale Image')
# cv2.namedWindow('Red Parts')
# cv2.namedWindow('Yellow Parts')
# cv2.namedWindow('Green Parts')
cv2.namedWindow('Customized Image')
cv2.namedWindow('Grayscale Trackbar')

# display windows
cv2.imshow('Original Image', original_image)
cv2.imshow('Grayscale Image',grayscale_image)

# create colored background
red_paper = eyw.create_colored_paper(original_image, 0,0,255)
yellow_paper = eyw.create_colored_paper(original_image, 0,255,255)
green_paper = eyw.create_colored_paper(original_image, 0,255,0)

# create grayscale trackbar
cv2.createTrackbar('red-yellow', 'Grayscale Trackbar', 200, 255, lambda x:None)
cv2.createTrackbar('yellow-green', 'Grayscale Trackbar', 100, 255, lambda x:None)

# instructions
print("After clicking on a window, use the following keyboard shortcuts:")
print("  's' to Save")
print("  'Esc' to Exit")

# color function
def getColor(r, g, b, break1, break2):
    paper = eyw.create_colored_paper(original_image, r, g, b)


# keyboard controls
keypressed = 1
while keypressed != 27 and keypressed != ord('s'):
    # color ratios
    break1 = cv2.getTrackbarPos('red-yellow', 'Grayscale Trackbar')
    break2 = cv2.getTrackbarPos('yellow-green', 'Grayscale Trackbar')

    redmin = [0, 0, 0]
    redmax = [break1, break1, break1]
    yellowmin = [break1 + 1, break1 + 1, break1 + 1]
    yellowmax = [break2, break2, break2]
    greenmin = [break2 + 1, break2 + 1, break2 + 1]
    greenmax = [255, 255, 255]

    # create masks for each color
    red_mask = eyw.create_mask(grayscale_image, redmin, redmax)
    yellow_mask = eyw.create_mask(grayscale_image, yellowmin, yellowmax)
    green_mask = eyw.create_mask(grayscale_image, greenmin, greenmax)

    # apply mask on top of colored background
    red_parts = eyw.apply_mask(red_paper, red_mask)
    yellow_parts = eyw.apply_mask(yellow_paper, yellow_mask)
    green_parts = eyw.apply_mask(green_paper, green_mask)

    # combines colors into single image
    customized_image1 = eyw.combine_images(red_parts, yellow_parts)
    customized_image2 = eyw.combine_images(customized_image1, green_parts)

    # cv2.imshow('Red Parts', red_parts)
    # cv2.imshow('Yellow Parts', yellow_parts)
    # cv2.imshow('Green Parts', green_parts)
    cv2.imshow('Customized Image', customized_image2)

    # keyboard input
    keypressed = cv2.waitKey(1)

if keypressed == 27: # close window if 'escape' key pressed
    cv2.destroyAllWindows()
    cv2.waitKey(1)
elif keypressed == ord('s'): # save greyscale and colored file if 's' key pressed
    file = filename.split('.')
    cv2.imwrite(file[0]+'Grayscale.'+file[1] ,grayscale_image)
    cv2.imwrite(file[0]+'RYG.'+file[1],customized_image2)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
