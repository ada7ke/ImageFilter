# imports
import cv2, eyw
import os.path
import json

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
print("  'e' to Import Data")
print("  's' to Save")
print("  'Esc' to Exit")

# create image windows
cv2.namedWindow('Original Image')
cv2.namedWindow('Grayscale Image')
cv2.namedWindow('Customized Image')
cv2.namedWindow('Color Trackbar')
cv2.namedWindow('Grayscale Trackbar')
cv2.namedWindow('Color Preview')

# create color trackbar
cv2.createTrackbar('color-select', 'Color Trackbar', 0, 5, lambda x:None)
cv2.createTrackbar('r', 'Color Trackbar', 0, 255, lambda x:None)
cv2.createTrackbar('g', 'Color Trackbar', 0, 255, lambda x:None)
cv2.createTrackbar('b', 'Color Trackbar', 0, 255, lambda x:None)

# create grayscale trackbar
cv2.createTrackbar('1', 'Grayscale Trackbar', 25, 255, lambda x:None)
cv2.createTrackbar('2', 'Grayscale Trackbar', 75, 255, lambda x:None)
cv2.createTrackbar('3', 'Grayscale Trackbar', 125, 255, lambda x:None)
cv2.createTrackbar('4', 'Grayscale Trackbar', 175, 255, lambda x:None)
cv2.createTrackbar('5', 'Grayscale Trackbar', 225, 255, lambda x:None)

# create color parts function
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

#initial color array
colors = [[245, 86, 78], [245, 124, 32], [247, 191, 5], [100, 207, 43], [43, 160, 207], [182, 104, 242]]

keypressed = 1
while keypressed != 27 and keypressed != ord('s'):
    # get selected color
    colorSelect = cv2.getTrackbarPos('color-select', 'Color Trackbar')
    # get rgb trackbar position and update the selected color
    colors[colorSelect] = [cv2.getTrackbarPos('b', 'Color Trackbar'), cv2.getTrackbarPos('g', 'Color Trackbar'),
                           cv2.getTrackbarPos('r', 'Color Trackbar'), ]

    # create color preview
    preview = eyw.create_colored_paper(original_image, *colors[colorSelect])
    preview = cv2.resize(preview, (125, 50), interpolation=cv2.INTER_AREA)

    # get breakpoints
    breaks = [cv2.getTrackbarPos('1', 'Grayscale Trackbar'), cv2.getTrackbarPos('2', 'Grayscale Trackbar'),
              cv2.getTrackbarPos('3', 'Grayscale Trackbar'), cv2.getTrackbarPos('4', 'Grayscale Trackbar'),
              cv2.getTrackbarPos('5', 'Grayscale Trackbar')]
    # create color parts
    colorParts = [getColor(*colors[0], -1, breaks[0]),
                  getColor(*colors[1], breaks[0], breaks[1]),
                  getColor(*colors[2], breaks[1], breaks[2]),
                  getColor(*colors[3], breaks[2], breaks[3]),
                  getColor(*colors[4], breaks[3], breaks[4]),
                  getColor(*colors[5], breaks[4], 255)]
    #combine images
    customized_image = combineImages(*colorParts)

    #show windows
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Grayscale Image', grayscale_image)
    cv2.imshow('Customized Image', customized_image)
    cv2.imshow('Color Preview', preview)

    # keyboard input
    keypressed = cv2.waitKey(1)

    # import color and breakpoint data
    if keypressed == ord('e'):
        data = input("Enter the filename of your data txt: ")
        if os.path.isfile(data) == True:
            with open(data, 'r') as f:
                breaks = json.loads(f.readline())
                colors = json.loads(f.readline())
        else:
            print("The filename was invalid")

if keypressed == 27:  # close window if 'escape' key pressed
    cv2.destroyAllWindows()
    cv2.waitKey(1)
elif keypressed == ord('s'):  # save greyscale, colored file, and data txt if 's' key pressed
    # create filenames
    file = filename.split('.')
    save_name = input("Enter a filename to save as or leave blank to use default name: ")
    if save_name == "":
        save_name = file[0]
    grayscale_file = save_name + 'Grayscale.' + file[1]
    colored_file = save_name + 'Colored.' + file[1]
    txt_file = save_name + 'Data.txt'

    # if filename already exists, add a number at the end
    index = 0
    while os.path.isfile(grayscale_file) == True or os.path.isfile(colored_file) == True or os.path.isfile(txt_file) == True:
        grayscale_file = save_name + 'Grayscale' + str(index) + '.' + file[1]
        colored_file = save_name + 'Colored' + str(index) + '.' + file[1]
        txt_file = save_name + 'Data' + str(index) + '.txt'
        index += 1

    #create files
    cv2.imwrite(grayscale_file, grayscale_image)
    cv2.imwrite(colored_file, customized_image)
    with open(txt_file, 'w') as f:
        json.dump(breaks, f); f.write("\n")
        json.dump(colors, f); f.write("\n")
    cv2.destroyAllWindows()
    cv2.waitKey(1)