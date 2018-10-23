# Background.jpg = picture of you 
# Foreground.png = shirt you want to try on

cp background.jpg ./resizedbackground.jpg
python fashion.py resizedbackground.jpg ./backgroundmask.jpg
python clothing.py resizedbackground.jpg foreground.png backgroundmask.jpg
