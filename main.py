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
    # filename = input("Enter the name of your file, including the "\
    #                              "extension, and then press 'enter': ")
    filename = "picture.jpg"
    if os.path.isfile(filename) == True:
        filename_valid = True
    else:
        print ("Something was wrong with that filename. Please try again.")

original_image = cv2.imread(filename,1)
grayscale_image_simple = cv2.imread(filename, 0)
grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

# instructions
print("After clicking on a window, use the following keyboard shortcuts:")
print("  's' to Save")
print("  'Esc' to Exit")

# create image windows
cv2.namedWindow('Original Image')
cv2.namedWindow('Grayscale Image')
cv2.namedWindow('Customized Image')
cv2.namedWindow('Color Trackbar')
cv2.namedWindow('Grayscale Trackbar')

# create color trackbar
cv2.createTrackbar('color-select', 'Color Trackbar', 0, 5, lambda x:None)
cv2.createTrackbar('r', 'Color Trackbar', 0, 255, lambda x:None)
cv2.createTrackbar('g', 'Color Trackbar', 0, 255, lambda x:None)
cv2.createTrackbar('b', 'Color Trackbar', 0, 255, lambda x:None)

# create grayscale trackbar
cv2.createTrackbar('1', 'Grayscale Trackbar', 50, 255, lambda x:None)
cv2.createTrackbar('2', 'Grayscale Trackbar', 100, 255, lambda x:None)
cv2.createTrackbar('3', 'Grayscale Trackbar', 150, 255, lambda x:None)
cv2.createTrackbar('4', 'Grayscale Trackbar', 200, 255, lambda x:None)
cv2.createTrackbar('5', 'Grayscale Trackbar', 250, 255, lambda x:None)

# color function
def getColor(r, g, b, b1, b2):
    paper = eyw.create_colored_paper(original_image, r, g, b)
    min = [b1+1, b1+1, b1+1]
    max = [b2, b2, b2]
    mask = eyw.create_mask(grayscale_image, min, max)
    colored_parts = eyw.apply_mask(paper, mask)
    return colored_parts

# combine colored images
def combineImages(i1, i2, i3, i4, i5, i6):
    customized_image1 = eyw.combine_images(i1, i2)
    customized_image2 = eyw.combine_images(customized_image1, i3)
    customized_image3 = eyw.combine_images(customized_image2, i4)
    customized_image4 = eyw.combine_images(customized_image3, i5)
    customized_image = eyw.combine_images(customized_image4, i6)
    return customized_image

colors = [[0, 0, 255], [0, 255, 255], [0, 255, 0], [100, 0, 255], [100, 255, 255], [0, 255, 100]]

# keyboard controls
keypressed = 1
while keypressed != 27 and keypressed != ord('s'):
    # get trackbar colors
    colorSelect = cv2.getTrackbarPos('color-select', 'Color Trackbar')
    colors[colorSelect] = [cv2.getTrackbarPos('b', 'Color Trackbar'), cv2.getTrackbarPos('g', 'Color Trackbar'),
                           cv2.getTrackbarPos('r', 'Color Trackbar'), ]

    # color ratios
    breaks = [cv2.getTrackbarPos('1', 'Grayscale Trackbar'), cv2.getTrackbarPos('2', 'Grayscale Trackbar'),
              cv2.getTrackbarPos('3', 'Grayscale Trackbar'), cv2.getTrackbarPos('4', 'Grayscale Trackbar'),
              cv2.getTrackbarPos('5', 'Grayscale Trackbar')]
    colorParts = [getColor(colors[0][0], colors[0][1], colors[0][2], -1, breaks[0]),
                  getColor(colors[1][0], colors[1][1], colors[1][2], breaks[0], breaks[1]),
                  getColor(colors[2][0], colors[2][1], colors[2][2], breaks[1], breaks[2]),
                  getColor(colors[3][0], colors[3][1], colors[3][2], breaks[2], breaks[3]),
                  getColor(colors[4][0], colors[4][1], colors[4][2], breaks[3], breaks[4]),
                  getColor(colors[5][0], colors[5][1], colors[5][2], breaks[4], 255)]

    customized_image = combineImages(colorParts[0], colorParts[1], colorParts[2], colorParts[3], colorParts[4], colorParts[5])

    cv2.imshow('Original Image', original_image)
    cv2.imshow('Grayscale Image', grayscale_image)
    cv2.imshow('Customized Image', customized_image)

    # keyboard input
    keypressed = cv2.waitKey(1)

if keypressed == 27: # close window if 'escape' key pressed
    cv2.destroyAllWindows()
    cv2.waitKey(1)
elif keypressed == ord('s'): # save greyscale and colored file if 's' key pressed
    file = filename.split('.')
    cv2.imwrite(file[0]+'Grayscale.'+file[1] ,grayscale_image)
    cv2.imwrite(file[0]+'RYG.'+file[1], customized_image)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
