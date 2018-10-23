from PIL import Image
import cv2
import numpy as np
import sys

# Author: Teryl Schmidt
# Contact: tschmidt6@wisc.edu
# Date: 2018

# How to run:
# python clothing.py [backgroundimage] [shirt to try on] [mask of background image]
# python clothing.py   background.jpg   foreground.png         myshirtmask.jpg

# IMPORTANT NOTE: Make sure [foreground.png] is a png with 4 channels and cropped correctly or it will not work
# print(foreground.shape) -> ( X , X , 4)
# Resizes background.jpg to 300 x 500 pixels because fashion.py only works with that size

# Outputs:
# boundingRectangle.jpg -> Shows where the algorithm thinks the shirt is in the picture with a blue rectangle
# resizedforeground.png -> Resized image that is the same size as the bounding box found in the previous file
# Output.jpg -> Shows the resized foreground picture placed ontop of the background picture in the bounding box area


# Function to overlay a transparent image on background
# https://pytech-solution.blogspot.com/2017/07/alphablending.html
def transparentOverlay(src , overlay , pos=(0,0),scale = 1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
    h,w,_ = overlay.shape  # Size of foreground
    rows,cols,_ = src.shape  # Size of background Image
    y,x = pos[0],pos[1]    # Position of foreground/overlay image
    
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
            src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
    return src

def main():
    try:

    # ----------------------- Read In The Files ----------------------- #

    	# Open the background picture (you standing there) 
        background = cv2.imread(sys.argv[1])

        # Open the foreground picture (the shirt you want to try on)
        foreground = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)

        # Open a copy of the foreground image using PIL (resizing function does not work with OpenCV)
        foregroundcopy = Image.open(sys.argv[2])


 	# NOTE: Requires the mask of the image generated using Fashion.py

 	# https://stackoverflow.com/questions/49098518/specifying-a-rectangle-around-a-binary-object-to-define-a-spatially-constrained
	# Put a bounding box around the ROI (Region of Intrest) in the backgroundmask.jpg
	# Gets the coordinates of the bounding box as:
	# x: Distance from the left side of background.jpg to the left edge of the bounding box
	# y: Distance from the top of background.jpg to the top edge of the bounding box
	# w: Total width of the bounding box
	# h: Total height of the bounding box

    # ----------------------- Put Bounding Box Around Object ----------------------- #
	backgroundmask = cv2.imread(sys.argv[3])
	active_px = np.argwhere(backgroundmask!=0)
	active_px = active_px[:,[1,0]]
	x,y,w,h = cv2.boundingRect(active_px)
	cv2.rectangle(backgroundmask,(x,y),(x+w,y+h),(255,0,0),1)
	cv2.imwrite('boundingRectangle.jpg', backgroundmask)


	# ----------------------- Resize Image ----------------------- #
	foregroundcopy = foregroundcopy.convert('RGBA')
	foregroundcopy.palette = None
	# Resize the foreground using width and height from bounding box and resize using Pillow function
	foregroundcopy = foregroundcopy.resize((w,h), Image.LANCZOS) 
	foregroundcopy = foregroundcopy.convert('P')
	foregroundcopy.save('resizedforeground.png')
	
	# Need to read in the file using cv2.imread with cv2.IMREAD_UNCHANGED so the OpenCV function works
	resizedforeground = cv2.imread('resizedforeground.png', cv2.IMREAD_UNCHANGED) 

	backgrond = cv2.resize(background, (300,500))


	# ----------------------- Place Image onto background ----------------------- #
	# Overlay the foreground image onto the background image where the bounding box (x,y) coordinates are
	output = transparentOverlay(background, resizedforeground, (x,y), 1)
	cv2.imwrite('Output.jpg', output)


	# ----------------------- Display the result ----------------------- # 
	# Comment this out if you don't want a popup window of the output
	cv2.imshow("Output" , output)
	cv2.waitKey()
	cv2.destroyAllWindows()

    except IOError:
        pass


if __name__ == "__main__":
    main()
