
This is a simple application to control the PC´s cursor with hand gestures shown to a camera using python. The instructions to make it work are listed below:

1. Clone the repository and move where is located:
	`$ cd location/of/the/repository`
	
2. Install the required libraries (here I'm using anaconda):
	`$ conda  install -c conda-forge --file requiremensts.txt`

3. Run the camouse.py script:
	`python camouse.py`
	
	It will pop two windows stacked one over the other (please slide them to show both on the screen).

	![](https://raw.githubusercontent.com/Sharmineroz/camera_mouse/master/screenshots/Screenshot%20%282%29.png)

4. Set the slidebars to values so that you see in the black/white image above almost only your hand in white color. Then in the other window select your hand clicking and dragging the cursor to form a frame containing the hand (the same way as one draws a square in paint)

	![](https://fthmb.tqn.com/8RXiZpXD8aWejfm2a74pOurmgyY=/400x0/id_anim_drawrect-56a246ba5f9b58b7d0c89194.gif)

	Then by typng "q", it will pop an image showing wour selection, if correct, type "q" again, if not, type "z" to select again.

	![](https://raw.githubusercontent.com/Sharmineroz/camera_mouse/master/screenshots/Screenshot%20%283%29.png)
	
5. If everything went right it deploys a window similar to the image below. Showing a red dot over the hand and a blue grid for location purposes.

![](https://raw.githubusercontent.com/Sharmineroz/camera_mouse/master/screenshots/Screenshot%20%284%29.png).

The cursor control works like a joystick, it moves the cursor only in the directions of the regions painted in green and one can only left or right click in the region painted in orange. Do a fist to right click and swearing gesture (all fingers together) to left click.

![](https://raw.githubusercontent.com/Sharmineroz/camera_mouse/master/screenshots/Screenshot%20%284%29%20-%20Copy.png)

![](https://raw.githubusercontent.com/Sharmineroz/camera_mouse/master/screenshots/untitled.png)

### Finaly, type "q" again to exit.
