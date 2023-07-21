import cv2
import numpy as np
import pandas as pd

# Image path
img_path = "C:/Users/furqan/Downloads/python-project-color-detection/colorpic.jpg"

# CSV path
csv_path = "C:/Users/furqan/Downloads/python-project-color-detection/c.csv"

# Reading the image  from the specified path with OpenCV and stores it in the img variable.

img = cv2.imread(img_path)

# Declaring global variables (used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and assigning column names
#function and assigns column names to the DataFrame.
csv = pd.read_csv(csv_path, header=None, names=['color_name', 'description', 'hex', 'R', 'G', 'B'])

# Cleaning Data of Wrong Format
#whitespaces and converts the color names to lowercase in the #'color_name' column.
csv['color_name'] = csv['color_name'].str.strip().str.lower()

# Fixing Wrong Data
#Removes the '#' character from the 'hex' column to clean the data.

csv['hex'] = csv['hex'].str.replace('#', '')

# Removing Duplicates
#Removes any duplicate rows from the DataFrame
csv = csv.drop_duplicates()

# Tidying up Fields in the Data
#Capitalizes the first letter of each word in the 'description' column.
csv['description'] = csv['description'].str.capitalize()

# Convert 'R', 'G', 'B' columns to integers, handling non-numeric values
def convert_to_int(value):
    #Tries to convert the value to an integer. If it fails, returns NaN ##(NumPy's representation of missing/NaN values).
    try:
        return int(value)
    except ValueError:
        return np.nan
#Applies the convert_to_int() function to the 'R', 'G', and 'B' columns of the DataFrame to convert their values to integers.

csv[['R', 'G', 'B']] = csv[['R', 'G', 'B']].applymap(convert_to_int)


# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    #to store the distances between the given color and the colors in the DataFrame.
    distances = []  # Initialize distances array
    for row in csv.itertuples(index=False):  # Iterate over each row in the csv DataFrame
        if pd.notna(row.R) and pd.notna(row.G) and pd.notna(row.B):  # Check for NaN values in 'R', 'G', 'B' columns not missing
            #Calculates the distance between the given RGB values and the RGB values in the current row of the DataFrame.
            d = abs(R - int(row.R)) + abs(G - int(row.G)) + abs(B - int(row.B))
            distances.append(d)  # Add the distance to the distances array
        else:
            distances.append(np.inf)  # Sets distance to infinity for missing values.


    index = np.argmin(distances)  # Finds the index of the minimum distance in the distances list.


    color_name = csv.loc[index, 'description']  # Get the color name corresponding to the minimum distance from the dataframe
    return color_name


# Function to get x, y coordinates of mouse double click
#Defines a callback function draw_function() to handle mouse events.
def draw_function(event, x, y, flags, param):
    #Checks if the event is a left mouse button double-click event.
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #Specifies that the variables are global, allowing them to be modified within the function.
        global b, g, r, xpos, ypos, clicked
        #to indicate that a double-click event occurred.
        clicked = True
        # Stores the x-coordinate of the double-clicked position
        xpos = x
        #Stores the y-coordinate of the double-clicked position.
        ypos = y
        #Retrieves the RGB values from the image at the double-clicked position.
        #In OpenCV, the cv2.imread() function reads an image in the BGR
        b, g, r = img[y, x]
        #Converts the RGB values to integers.
        b = int(b)
        g = int(g)
        r = int(r)

#Creates a window with the name 'image'.
cv2.namedWindow('image')
#Sets the mouse callback function to draw_function() for the 'image' window.
cv2.setMouseCallback('image', draw_function)
#Enters an infinite loop for continuously displaying the image and detecting mouse events.
while True:
    #Displays the image in the 'image' window.

    cv2.imshow("image", img)
#Checks if a double-click event occurred.
    if clicked:
        #Draws a filled rectangle on the image with the color specified by the RGB values.

        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
#Calls the getColorName() function to get the color name and creates a text string with the RGB values.
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        #Writes the color name and RGB values on the image.
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
#Checks if the sum of the RGB values is greater than or equal to 600.
        if r + g + b >= 600:
            #Writes the color name and RGB values on the image with a different color if the sum is greater than or equal to 600.

            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
#Resets the clicked variable to False to indicate that the double-click event has been processed.
        clicked = False
#Waits for a keyboard event for 20 milliseconds. If the key pressed is ESC (ASCII code 27), breaks the loop and exits the program.

    if cv2.waitKey(20) & 0xFF == 27:
        break
#Closes all OpenCV windows and destroys the window objects
cv2.destroyAllWindows()

# Print the cleaned data
print(csv)
