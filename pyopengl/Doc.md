# Documentation

--- 

## Creating a window

To create a window, you need to instantiate the pydraw class. For that you need to import the pydraw module with the ```import pydraw``` line.

Then create the instance of the window as following. You need to paste the following parameters ````window size x````, ```window size y``` and ```window name```.

````python
import pydraw as pdw

pydraw = pdw.Pydraw(1080, 720, "My Pydraw Window")
````

Now that our window is opened, we need to keep it alive by creating a loop that will be the frames of our application.
For that, we will be using the ````pydraw.window_is_open()```` methode as the condition of our while loop.
We will then have to worry about when the frame starts and when it ends. For that we'll use the ````pydraw.start_frame()```` and the ````pydraw.end_frame()```` methods as following:

````python
import pydraw as pdw

pydraw = pdw.Pydraw(1080, 720, "My Pydraw Window")
while pydraw.window_is_open():
    pydraw.start_frame()

    pydraw.end_frame()
````

We now have a working empty window that we can close.

## Flags

When creating a window, you can add flags to the process to make it as close as your need as possible.
Here is a list of the flags that you can use:

````python
pydraw.RESIZABLE
pydraw.V_SYNC_OFF
pydraw.FULLSCREEN
````

There are also secondary flags that come *AFTER* the primary ones. Those are:
```python
max_fps= int
window_pos= tuple[2]
cursor= 0 <= int <= 2
```

## Displaying images

Now that your window is created according to your needs, you might want to display images.
For that you need to load you image and define the points where it will be displayed.
To load an image, you use the ````pydraw.load_image()````. This methode uses the filepath to load the image and returns an object image.

````python
my_image = pydraw.load_image("you_image_path")
````

To display it, you now have to define its four corners' positions.
The position is a value between 0 and the size of you window. 0 is in the top left corner of the screen and increases to the right corner.
For that, you will use the ````set_pos()```` method of your image. The arguments that this method needs are the following:
The four corners coordinate in a clockwise way starting from the topleft corner:

topleft corner, topright corner, bottomright corner, bottomleft corner, window_size

````python
my_image.set_pos((0, 0), (1080, 0), (1080, 720), (0, 720), pydraw.get_window_size())
````

Now to display the image, you just need to tell the engine to draw it every frame. Add the following line to the loop:

````python
pydraw.draw_image(my_image)
````

## Game logic

For the game logic, there are lots of methods you can use. Here is a list of said method and what they do:

````python
pydraw.hide_cursor()  # Hides the cursor
pydraw.disable_cursor()  # Disables the cursor
pydraw.show_cursor()  # Shows the cursor
pydraw.set_max_fps()  # Sets the max framerate
pydraw.get_window_size()  # Returns the size of the window
pydraw.set_cursor_position()  # Returns the position of the cursor
pydraw.get_events()  # Returns a list of events

my_image.flip_top()  # Flips the image from the top
my_image.flip_left()  # Flips the image from the left
````
