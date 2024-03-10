import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np

class DisplayModule:
    def __init__(self):
        # Initialize GLFW
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # Creating a window
        self.window = glfw.create_window(640, 480, "PyOpenGL Window", None, None)

        # Check if the window couldn't be created
        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)

        # Make the context current
        glfw.make_context_current(self.window)


def load_image(filename: str):
    image = Image.open("image_test.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image
    image_data = image.convert("RGBA").tobytes()

