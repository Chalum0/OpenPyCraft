import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import time

import pydrawImage
import pydrawInput

RESIZABLE = "resizable"
V_SYNC_OFF = "v_sync_off"
FULLSCREEN = "fullscreen"


class Pydraw:
    def __init__(self, window_width, window_height, window_title="OpenGL Window",
                 *flags, max_fps=None, window_pos=(400, 200), cursor=0):
        self._k = None
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        flags_set = set(flags)
        resizable = "resizable" in flags_set
        fullscreen = "fullscreen" in flags_set
        v_sync = "v_sync_off" not in flags_set

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

        glfw.set_window_pos(self.window, window_pos[0], window_pos[1])
        glfw.make_context_current(self.window)

        # Initialize texture ID
        self.textures = {}  # Changed to a dictionary to handle multiple textures
        self.texture_counter = 0

        self.max_fps = max_fps
        self.start_time = None
        self.desired_frame_time = None

        self.events = []

        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        if not v_sync:
            glfw.swap_interval(0)

        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        # Initialize cursor position
        self.cursor_position = (0, 0)

        # Set up a cursor position callback
        glfw.set_cursor_pos_callback(self.window, self.cursor_position_callback)

        self.MOUSE_BUTTON_DOWN, self.MOUSE_BUTTON_UP, self.KEY_DOWN, self.KEY_UP = ("self.MOUSE_BUTTON_DOWN", "self.MOUSE_BUTTON_UP", "self.Key_DOWN", "self.KEY_UP")
        self._keys = pydrawInput.keys

        self.key = pydrawInput.Keys(self._keys)
        self.mouse = pydrawInput.Mouse()

        for key in self._keys:
            setattr(self, key, f"{key}")

        if cursor == 0:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)  # Sets the cursor as normal
        elif cursor == 1:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)  # Sets the cursor as hidden
        elif cursor == 2:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)  # Locks the cursor on the window

    def hide_cursor(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)  # Sets the cursor as hidden

    def disable_cursor(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)  # Locks the cursor on the window

    def show_cursor(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)  # Sets the cursor as normal

    def load_image(self, image_path):
        """
        Load an image from the specified image_path and return an instance of pydrawImage.Image.

        Parameters:
            image_path (str): The path to the image file.

        Returns:
            pydrawImage.Image: An instance of pydrawImage.Image representing the loaded image.

        """
        image = Image.open(image_path)  # Open the image from the file path
        image_data = image.convert("RGBA").tobytes()  # Convert the image to RGBA format and get the raw bytes

        texture = glGenTextures(1)  # Generate a unique OpenGL texture ID
        glBindTexture(GL_TEXTURE_2D, texture)  # Bind the newly generated texture ID as the active 2D texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     image_data)  # Load the texture into the active texture slot with parameters for how to scale the texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR)  # Set the texture sampling parameters for minification (when texture needs to be scaled down)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        GL_LINEAR)  # Set the texture sampling parameters for magnification (when texture needs to be scaled up)

        image_key = self.texture_counter + 1  # Generate a unique key for the texture for our internal tracking
        self.texture_counter += 1  # Increment the counter for the next time we load a texture
        self.textures[image_key] = (texture, image.width, image.height)  # Store the OpenGL texture ID, the width, and the height of the image in our internal dictionary using the generated key
        # Return a new Image object that is tagged with the generated key
        return pydrawImage.Image(image_key)

    def draw_image(self, image, position=None):
        """
        Draws an image on the window.

        Parameters:
        - image: An instance of the Image class representing the image to be drawn.
        - position (optional): A list containing the position of the image's top left corner in window coordinates.

        Returns:
        None
        """
        # Retrieve the OpenGL texture ID, width, and height for the image from the internal dictionary using the image's key (ID)
        texture, img_width, img_height = self.textures[image.get_id()]
        glEnable(GL_TEXTURE_2D)  # Retrieve the OpenGL texture ID, width, and height for the image from the internal dictionary using the image's key (ID)
        glBindTexture(GL_TEXTURE_2D, texture)  # Bind the texture object to the active texture unit
        # Begin defining the polygon (GL_QUADS specifies that we are drawing a quadrilateral i.e., a square or rectangle, which is what the image will map onto)
        glBegin(GL_QUADS)

        # If a position for the image has been specified
        if not not position:
            # Set the position of the image - this adjusts the attributes of the image so that it will be rendered at the correct location in the window
            image.set_pos(position[0], position[1], position[2], position[3], glfw.get_window_size(self.window))

        # Define the four corners of the quadrilateral which are mapped
        # to the corners of the texture image. The functions glTexCoord2f
        # specify the texture coordinates and glVertex2f specify the actual
        # vertex positions. The texture coordinates range from 0.0 to 1.0,
        # where 0.0 represents the top or left edge of the texture image,
        # and 1.0 represents the bottom or right edge.
        glTexCoord2f(0, 0); glVertex2f(*image.ndc_top_left)
        glTexCoord2f(1, 0); glVertex2f(*image.ndc_top_right)
        glTexCoord2f(1, 1); glVertex2f(*image.ndc_bottom_right)
        glTexCoord2f(0, 1); glVertex2f(*image.ndc_bottom_left)
        # Finish defining the polygon
        glEnd()

    def set_filter(self, filter):
        r, g, b = self.convert_rgb(filter)
        # print(r, g, b)
        # r, g, b = (1, 1, 1)
        glColor4f(r, g, b, 0)

    def draw_polygons(self, image, positions, filters):
        texture, img_width, img_height = self.textures[image.get_id()]
        glEnable(GL_TEXTURE_2D)  # Retrieve the OpenGL texture ID, width, and height for the image from the internal dictionary using the image's key (ID)
        glBindTexture(GL_TEXTURE_2D, texture)  # Bind the texture object to the active texture unit
        # Begin defining the polygon (GL_QUADS specifies that we are drawing a quadrilateral i.e., a square or rectangle, which is what the image will map onto)
        glBegin(GL_QUADS)
        for i in range(len(positions)):
            self.set_filter(filters[i])
            self._draw_polygon(image, positions[i])
        glEnd()

        self.set_filter((0, 0, 0))

    def _draw_polygon(self, image, position):
        image.set_pos(position[0], position[1], position[2], position[3], glfw.get_window_size(self.window))
        glTexCoord2f(0, 0); glVertex2f(*image.ndc_top_left)
        glTexCoord2f(1, 0); glVertex2f(*image.ndc_top_right)
        glTexCoord2f(1, 1); glVertex2f(*image.ndc_bottom_right)
        glTexCoord2f(0, 1); glVertex2f(*image.ndc_bottom_left)

    def set_max_fps(self, max_fps):
        """
        Set the maximum frames per second (FPS) for the application.

        :param max_fps: The desired maximum FPS for the application.
        :type max_fps: int

        :return: None
        """
        self.max_fps = max_fps

    def start_frame(self):
        """

        Starts a new frame by initializing the required variables and clearing the color buffer.

        Parameters:
            - self: The reference to the current instance of the class.

        Returns:
            None

        """
        if not not self.max_fps:
            self.desired_frame_time = 1.0 / self.max_fps

        self.start_time = time.time()

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)

    def fill(self, rgb=(135, 206, 235)):
        r, g, b = self.convert_rgb(rgb)
        glClearColor(r, g, b, 1)

    def convert_rgb(self, rgb):
        r, g, b = rgb
        return r/255, g/255, b/255

    def end_frame(self):
        """
        Ends the current frame by swapping the buffers and handling frame rate control.

        - This method is typically called at the end of each frame in a rendering loop.

        Parameters:
            - self: the instance of the class that the method belongs to.

        Returns:
            - None

        Example usage:
            end_frame()
        """
        glfw.swap_buffers(self.window)

        if not not self.max_fps:
            elapsed_time = time.time() - self.start_time
            time_to_sleep = self.desired_frame_time - elapsed_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        self.events = []

    def quit(self):
        self.window = None
        glfw.terminate()

    def window_is_open(self):
        return not glfw.window_should_close(self.window)

    def get_window_size(self):
        return glfw.get_window_size(self.window)

    def mouse_button_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.events.append(pydrawInput.Event(self.MOUSE_BUTTON_DOWN))
            if button == glfw.MOUSE_BUTTON_1:
                self.mouse.mouse_button_pressed(0)
            elif button == glfw.MOUSE_BUTTON_2:
                self.mouse.mouse_button_pressed(1)
            elif button == glfw.MOUSE_BUTTON_3:
                self.mouse.mouse_button_pressed(2)
            elif button == glfw.MOUSE_BUTTON_4:
                self.mouse.mouse_button_pressed(3)
            elif button == glfw.MOUSE_BUTTON_5:
                self.mouse.mouse_button_pressed(4)
            elif button == glfw.MOUSE_BUTTON_6:
                self.mouse.mouse_button_pressed(5)
            elif button == glfw.MOUSE_BUTTON_7:
                self.mouse.mouse_button_pressed(6)
            elif button == glfw.MOUSE_BUTTON_8:
                self.mouse.mouse_button_pressed(7)


        elif action == glfw.RELEASE:
            self.events.append(pydrawInput.Event(self.MOUSE_BUTTON_UP))
            if button == glfw.MOUSE_BUTTON_1:
                self.mouse.mouse_button_released(0)
            elif button == glfw.MOUSE_BUTTON_2:
                self.mouse.mouse_button_released(1)
            elif button == glfw.MOUSE_BUTTON_3:
                self.mouse.mouse_button_released(2)
            elif button == glfw.MOUSE_BUTTON_4:
                self.mouse.mouse_button_released(3)
            elif button == glfw.MOUSE_BUTTON_5:
                self.mouse.mouse_button_released(4)
            elif button == glfw.MOUSE_BUTTON_6:
                self.mouse.mouse_button_released(5)
            elif button == glfw.MOUSE_BUTTON_7:
                self.mouse.mouse_button_released(6)
            elif button == glfw.MOUSE_BUTTON_8:
                self.mouse.mouse_button_released(7)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            for i in self._keys:
                exec(f"self._k = glfw.{i}")
                if key == self._k:
                    self.events.append(pydrawInput.Event(self.KEY_DOWN, key=i))
                    self.key.k_pressed(i)
        if action == glfw.RELEASE:
            for i in self._keys:
                exec(f"self._k = glfw.{i}")
                if key == self._k:
                    self.events.append(pydrawInput.Event(self.KEY_UP, key=i))
                    self.key.k_released(i)

    def cursor_position_callback(self, window, xpos, ypos):
        self.mouse.update_pos(xpos, ypos)

    def set_cursor_position(self, x, y):
        glfw.set_cursor_pos(self.window, x, y)
        self.mouse.update_pos(x, y)

    def get_events(self):
        return self.events
