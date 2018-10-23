==========================================
SOFTWARE REQUIREMENTS
==========================================
OpenCV
Keras with Tensorflow backend
Pandas
NumPy
Pillow

==========================================
HOW TO RUN
==========================================

SCRIPT
-------------
sh runClothing.sh

sh Clean.sh


FOR TESTING
-------------
python fashion.py background.jpg ./backgroundmask.jpg

python clothing.py background.jpg foreground.png background mask.jpg


IMPORTANT NOTE: Make sure [shirt to try on] is a PNG with 4 channels and cropped correctly or it will not work
		print(foreground.shape) should print out -> ( X , X , 4)

		Also the background.jpg can only be 300 x 500 pixels or a index out of bounds exception will be thrown, the program will 				resize it for you.


OUTPUT FILES
-------------
backgroundMask.jpg -> Extracts the shirt out of the image
boundingRectangle.jpg -> Shows where the algorithm thinks the shirt is in the program with a blue rectangle
Output.jpg -> Shows the resized foreground picture placed on top of the background picture in the bounding box area


