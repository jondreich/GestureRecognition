# Gesture Recognition For CS390
This was my final project for CS390 (Machine Perception)
###Installation Guide
- Make sure you have Python version 3.1 or higher.
- Run the following
-- `git clone https://github.com/jondreich/GestureRecognition.git && cd GestureRecognition`
-- `python3 run.py`
- It should just work but if it doesnt ¯\\_(ツ)_/¯

## Report
###Concept
Gesture recognition based on the contours of a hand.
###Issues and Removed Feature Ideas
- Hand identification based on skin color.
-- I tried to do this by capturing a small square where the hand was expected to be, and then using that to (hopefully) find the entire hand.
-- This almost never worked and I couldn't figure out why.
-- I think it had something to do with the color of the hand not staying the same between frames because of lightning.
- More accurate recognition based on distances between minima and edge of hull
-- Sometimes random minima were included in weird places (usually around the wrist) which made everything less accurate, not more

