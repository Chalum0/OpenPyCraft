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

    def set_pos(self, topleft, topright, bottomright, bottomleft, window_size):
        def to_ndc(x, y):
            ndc_x = (x / window_size[0]) * 2 - 1
            ndc_y = (y / window_size[1]) * -2 + 1  # Invert y-axis
            return ndc_x, ndc_y

        # Convert all four points to NDC
        self.ndc_top_left = to_ndc(*topleft)
        self.ndc_top_right = to_ndc(*topright)
        self.ndc_bottom_right = to_ndc(*bottomright)
        self.ndc_bottom_left = to_ndc(*bottomleft)

        if self.flipped_top:
            self.ndc_top_left, self.ndc_bottom_left = self.ndc_bottom_left, self.ndc_top_left
            self.ndc_top_right, self.ndc_bottom_right = self.ndc_bottom_right, self.ndc_top_right

        if self.flipped_side:
            self.ndc_top_left, self.ndc_top_right = self.ndc_top_right, self.ndc_top_left
            self.ndc_bottom_left, self.ndc_bottom_right = self.ndc_bottom_right, self.ndc_bottom_left
