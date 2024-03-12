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