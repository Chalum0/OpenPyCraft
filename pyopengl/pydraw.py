import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import time

import pydrawImage


class SimpleOpenGLImageRenderer:
    def __init__(self, window_width, window_height, window_title="OpenGL Window", max_fps=None, resizable=False,
                 v_sync=True, fullscreen=False):
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        if not resizable:
            glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

        if not fullscreen:
            self.window_width = window_width
            self.window_height = window_height
            self.window = glfw.create_window(window_width, window_height, window_title, None, None)
        else:
            primary_monitor = glfw.get_primary_monitor()
            video_mode = glfw.get_video_mode(primary_monitor)
            self.window_width = video_mode.size.width
            self.window_height = video_mode.size.height
            self.window = glfw.create_window(self.window_width, self.window_height, window_title, primary_monitor, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.make_context_current(self.window)

        # Initialize texture ID
        self.textures = {}  # Changed to a dictionary to handle multiple textures
        self.texture_counter = 0

        self.max_fps = max_fps
        self.start_time = None
        self.desired_frame_time = None

        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        if not v_sync:
            glfw.swap_interval(0)

    def load_image(self, image_path):
        image = Image.open(image_path)
        # image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = image.convert("RGBA").tobytes()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image_key = self.texture_counter + 1
        self.texture_counter += 1
        self.textures[image_key] = (texture, image.width, image.height)
        return pydrawImage.Image(image_key)

    def draw_image(self, image, position=None):
        texture, img_width, img_height = self.textures[image.get_id()]
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)

        window_width, window_height = glfw.get_window_size(self.window)
        h_window_width, h_window_height = (window_width/2, window_height/2)

        glTexCoord2f(0, 0); glVertex2f(*image.ndc_top_left)
        glTexCoord2f(1, 0); glVertex2f(*image.ndc_top_right)
        glTexCoord2f(1, 1); glVertex2f(*image.ndc_bottom_right)
        glTexCoord2f(0, 1); glVertex2f(*image.ndc_bottom_left)
        glEnd()

    def set_max_fps(self, max_fps):
        self.max_fps = max_fps

    def start_frame(self):
        if not not self.max_fps:
            self.desired_frame_time = 1.0 / self.max_fps

        self.start_time = time.time()

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)

    def end_frame(self):
        glfw.swap_buffers(self.window)

        if not not self.max_fps:
            elapsed_time = time.time() - self.start_time
            time_to_sleep = self.desired_frame_time - elapsed_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

    def quit(self):
        glfw.terminate()

    def window_is_open(self):
        return not glfw.window_should_close(self.window)

    def get_window_size(self):
        return glfw.get_window_size(self.window)
