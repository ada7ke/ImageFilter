# imports
import cv2, eyw, os.path, json

# get image file
print("Save your original image in the same folder as this program.")
filename_valid = False
while not filename_valid:
    filename = "picture.jpg"
    if os.path.isfile(filename):
        filename_valid = True
    else:
        print("Something was wrong with that filename. Please try again.")

# read image files
original_image = cv2.imread(filename, 1)
grayscale_image_simple = cv2.imread(filename, 0)

# convert to grayscale
grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)

# instructions
print("Use the Color Trackbar window to select the color swatch to change, and change the RGB values")
print("Use the Grayscale Trackbar window to change the breakpoints between the different colors")
print("After clicking on a window, use the following keyboard shortcuts:")
print("  'i' to Import Data")
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
cv2.createTrackbar('color-count', 'Color Trackbar', 6, 9, lambda x: None)   # number of colors
cv2.createTrackbar('color-select', 'Color Trackbar', 1, 9, lambda x: None)  # 1-based index
cv2.createTrackbar('r', 'Color Trackbar', 0, 255, lambda x: None)
cv2.createTrackbar('g', 'Color Trackbar', 0, 255, lambda x: None)
cv2.createTrackbar('b', 'Color Trackbar', 0, 255, lambda x: None)

# create grayscale trackbar
cv2.createTrackbar('breakpoint-select', 'Grayscale Trackbar', 1, 8, lambda x: None)  # 1-based index
cv2.createTrackbar('breakpoint', 'Grayscale Trackbar', 100, 255, lambda x: None)

# create color parts function
def getColor(r, g, b, b1, b2):
    paper = eyw.create_colored_paper(original_image, r, g, b)
    minv = [b1 + 1, b1 + 1, b1 + 1]
    maxv = [b2, b2, b2]
    mask = eyw.create_mask(grayscale_image, minv, maxv)
    colored_parts = eyw.apply_mask(paper, mask)
    return colored_parts

# combine colored images
def combineImages(colorParts):
    combined = colorParts[0].copy()
    for i in range(1, len(colorParts)):
        combined = eyw.combine_images(combined, colorParts[i])
    return combined

# initial arrays
colors = [
    [245, 86, 78], [245, 124, 32], [247, 191, 5],
    [100, 207, 43], [43, 160, 207], [182, 104, 242],
    [82, 58, 183], [173, 84, 12], [83, 90, 123],
    [233, 71, 18]
]
breaks = [25, 50, 75, 100, 125, 150, 175, 200, 225]

tempc = -1
tempb = -1
keypressed = 1

# program loop
while keypressed not in (27, ord('s')):
    # number of colors
    colorCount = cv2.getTrackbarPos('color-count', 'Color Trackbar')
    if colorCount < 1:
        colorCount = 1

    # color select
    colorSelect_ui = cv2.getTrackbarPos('color-select', 'Color Trackbar')
    if colorSelect_ui < 1:
        colorSelect_ui = 1
    elif colorSelect_ui > colorCount:
        colorSelect_ui = colorCount
    cv2.setTrackbarPos('color-select', 'Color Trackbar', colorSelect_ui)
    colorSelect = colorSelect_ui - 1  # 0-based

    # breakpoint select
    breakpointSelect_ui = cv2.getTrackbarPos('breakpoint-select', 'Grayscale Trackbar')
    bp_max_ui = max(1, colorCount - 1)
    if breakpointSelect_ui < 1:
        breakpointSelect_ui = 1
    elif breakpointSelect_ui > bp_max_ui:
        breakpointSelect_ui = bp_max_ui
    cv2.setTrackbarPos('breakpoint-select', 'Grayscale Trackbar', breakpointSelect_ui)
    breakpointSelect = breakpointSelect_ui - 1  # 0-based

    # update color trackbar if switching color
    if colorSelect != tempc:
        cv2.setTrackbarPos('b', 'Color Trackbar', colors[colorSelect][0])
        cv2.setTrackbarPos('g', 'Color Trackbar', colors[colorSelect][1])
        cv2.setTrackbarPos('r', 'Color Trackbar', colors[colorSelect][2])
        tempc = colorSelect

    # update selected color from sliders
    colors[colorSelect] = [
        cv2.getTrackbarPos('b', 'Color Trackbar'),
        cv2.getTrackbarPos('g', 'Color Trackbar'),
        cv2.getTrackbarPos('r', 'Color Trackbar'),
    ]

    # color preview
    preview = eyw.create_colored_paper(original_image, *colors[colorSelect])
    preview = cv2.resize(preview, (125, 50), interpolation=cv2.INTER_AREA)

    # update breakpoint slider
    if breakpointSelect != tempb and breakpointSelect < len(breaks):
        cv2.setTrackbarPos('breakpoint', 'Grayscale Trackbar', breaks[breakpointSelect])
        tempb = breakpointSelect

    if breakpointSelect < len(breaks):
        breaks[breakpointSelect] = cv2.getTrackbarPos('breakpoint', 'Grayscale Trackbar')

    # create color parts
    colorParts = [getColor(*colors[0], -1, breaks[0])]
    for i in range(colorCount - 2):
        colorParts.append(getColor(*colors[i + 1], breaks[i], breaks[i + 1]))
    colorParts.append(getColor(*colors[colorCount - 1], breaks[colorCount - 2], 255))

    # combine color parts
    customized_image = combineImages(colorParts)

    # show windows
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Grayscale Image', grayscale_image)
    cv2.imshow('Customized Image', customized_image)
    cv2.imshow('Color Preview', preview)

    # wait for user input
    keypressed = cv2.waitKey(1)

    # import data
    if keypressed == ord('i'):
        data = "pictureData.txt"
        if os.path.isfile(data):
            with open(data, 'r') as f:
                # loads break and color data
                breaks = json.loads(f.readline())
                colors = json.loads(f.readline())
                colorCount = len(colors)

                # reset trackbars to match newly imported data
                cv2.setTrackbarPos('color-count', 'Color Trackbar', colorCount)
                cv2.setTrackbarPos('color-select', 'Color Trackbar', 1)
                cv2.setTrackbarPos('b', 'Color Trackbar', colors[0][0])
                cv2.setTrackbarPos('g', 'Color Trackbar', colors[0][1])
                cv2.setTrackbarPos('r', 'Color Trackbar', colors[0][2])
                cv2.setTrackbarPos('breakpoint-select', 'Grayscale Trackbar', 1)
                cv2.setTrackbarPos('breakpoint', 'Grayscale Trackbar', breaks[0])
                tempc = 0

                # adds empty colors and breakpoints to allow adding colors again
                while len(colors) < 10:
                    colors.append([0, 0, 0])
                    breaks.append(255)
        else:
            print("The filename was invalid")

# exit / save
if keypressed == 27:  # ESC
    cv2.destroyAllWindows()
    cv2.waitKey(1)
elif keypressed == ord('s'):  # save
    # create file names
    file = filename.split('.')
    save_name = input("Enter a filename to save as or leave blank to use default name: ")
    if save_name == "":
        save_name = file[0]
    grayscale_file = save_name + 'Grayscale.' + file[1]
    colored_file = save_name + 'Colored.' + file[1]
    txt_file = save_name + 'Data.txt'

    # ensure file names don't exist
    index = 0
    while os.path.isfile(grayscale_file) or os.path.isfile(colored_file) or os.path.isfile(txt_file):
        grayscale_file = save_name + 'Grayscale' + str(index) + '.' + file[1]
        colored_file = save_name + 'Colored' + str(index) + '.' + file[1]
        txt_file = save_name + 'Data' + str(index) + '.txt'
        index += 1

    # write files
    cv2.imwrite(grayscale_file, grayscale_image)
    cv2.imwrite(colored_file, customized_image)
    with open(txt_file, 'w') as f:
        json.dump(breaks, f); f.write("\n")
        json.dump(colors, f); f.write("\n")
    cv2.destroyAllWindows()
    cv2.waitKey(1)
