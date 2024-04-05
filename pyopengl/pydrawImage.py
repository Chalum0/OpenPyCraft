class Image:
    def __init__(self, image_id):
        self.ndc_bottom_left = None
        self.ndc_bottom_right = None
        self.ndc_top_right = None
        self.ndc_top_left = None
        self._image_id = image_id
        self.flipped_top = False
        self.flipped_side = False

    def flip_top(self):
        self.flipped_top = not self.flipped_top

    def flip_side(self):
        self.flipped_side = not self.flipped_side

    def get_id(self):
        return self._image_id

    def apply_texture_parameters(self):
        glBindTexture(GL_TEXTURE_2D, self._image_id)
        wrap_s = globals().get(self.texture_wrap_s, GL_REPEAT)
        wrap_t = globals().get(self.texture_wrap_t, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_t)
        glBindTexture(GL_TEXTURE_2D, 0)

    def set_pos(self, topleft, topright, bottomright, bottomleft, window_size):
        def to_ndc(x, y, window_s):
            if window_s[0] == 0:
                window_s = (1, window_s[1])
            if window_s[1] == 0:
                window_s = (window_s[0], 1)

            ndc_x = (x / window_s[0]) * 2 - 1
            ndc_y = (y / window_s[1]) * -2 + 1  # Invert y-axis
            return ndc_x, ndc_y

        # Convert all four points to NDC
        self.ndc_top_left = to_ndc(*topleft, window_size)
        self.ndc_top_right = to_ndc(*topright, window_size)
        self.ndc_bottom_right = to_ndc(*bottomright, window_size)
        self.ndc_bottom_left = to_ndc(*bottomleft, window_size)

        if self.flipped_top:
            self.ndc_top_left, self.ndc_bottom_left = self.ndc_bottom_left, self.ndc_top_left
            self.ndc_top_right, self.ndc_bottom_right = self.ndc_bottom_right, self.ndc_top_right

        if self.flipped_side:
            self.ndc_top_left, self.ndc_top_right = self.ndc_top_right, self.ndc_top_left
            self.ndc_bottom_left, self.ndc_bottom_right = self.ndc_bottom_right, self.ndc_bottom_left
