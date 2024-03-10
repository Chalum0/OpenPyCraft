import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import time

class SimpleOpenGLImageRenderer:
    def __init__(self, window_width, window_height, window_title="OpenGL Window"):
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        self.window_width = window_width
        self.window_height = window_height
        self.window = glfw.create_window(window_width, window_height, window_title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.make_context_current(self.window)

        # Initialize texture ID
        self.texture = glGenTextures(1)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = image.convert("RGBA").tobytes()

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw_image(self, left, bottom, right, top):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(left, bottom)
        glTexCoord2f(1, 0); glVertex2f(right, bottom)
        glTexCoord2f(1, 1); glVertex2f(right, top)
        glTexCoord2f(0, 1); glVertex2f(left, top)
        glEnd()

    def start_render_loop(self, max_fps=60.0):
        desired_frame_time = 1.0 / max_fps

        while not glfw.window_should_close(self.window):
            start_time = time.time()

            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)

            # Adjust these values as needed
            self.draw_image(-1, -1, 1, 1)

            glfw.swap_buffers(self.window)

            elapsed_time = time.time() - start_time
            time_to_sleep = desired_frame_time - elapsed_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        glfw.terminate()


# Usage example :
if __name__ == "__main__":
    renderer = SimpleOpenGLImageRenderer(640, 480, "Simple OpenGL Renderer")
    renderer.load_image("image_test.png")  # Specify the path to your image
    renderer.start_render_loop()
