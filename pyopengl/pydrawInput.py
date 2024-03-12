class Keys:
    def __init__(self, keys):
        self.pressed = {}
        for key in keys:
            self.pressed[key] = False

    def get_pressed(self):
        return self.pressed

    def key_pressed(self, key):
        self.pressed[key] = True

    def key_released(self, key):
        self.pressed[key] = False


class Key:
    def __init__(self, id):
        self._id = id


class Mouse:
    def __init__(self):
        self._pressed = [False for i in range(8)]

    def _set_to_false(self):
        self._pressed = [False for i in range(8)]

    def get_pressed(self, length=3):
        if length >= 8:
            return self._pressed[:8]
        elif not length <= 3:
            return self._pressed[:length]


class Event:
    def __init__(self, type, key=None):
        self.type = type
        self.key = key


keys = [
    "KEY_A", "KEY_B", "KEY_C", "KEY_D", "KEY_E", "KEY_F", "KEY_G", "KEY_H", "KEY_I", "KEY_J", "KEY_K", "KEY_L",
    "KEY_M", "KEY_N", "KEY_O", "KEY_P", "KEY_Q", "KEY_R", "KEY_S", "KEY_T", "KEY_U", "KEY_V", "KEY_W", "KEY_X",
    "KEY_Y", "KEY_Z",

    "KEY_0", "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9",

    "KEY_F1", "KEY_F2", "KEY_F3", "KEY_F4", "KEY_F5", "KEY_F6", "KEY_F7", "KEY_F8", "KEY_F9", "KEY_F10", "KEY_F11",
    "KEY_F12", "KEY_F13", "KEY_F14", "KEY_F15", "KEY_F16", "KEY_F17", "KEY_F18", "KEY_F19", "KEY_F20", "KEY_F21",
    "KEY_F22", "KEY_F23", "KEY_F24", "KEY_F25",

    "KEY_ESCAPE",
    "KEY_ENTER",
    "KEY_TAB",
    "KEY_BACKSPACE",
    "KEY_INSERT",
    "KEY_DELETE",
    "KEY_RIGHT",
    "KEY_LEFT",
    "KEY_DOWN",
    "KEY_UP",
    "KEY_PAGE_UP",
    "KEY_PAGE_DOWN",
    "KEY_HOME",
    "KEY_END",
    "KEY_CAPS_LOCK",
    "KEY_SCROLL_LOCK",
    "KEY_NUM_LOCK",
    "KEY_PRINT_SCREEN",
    "KEY_PAUSE",
    "KEY_LEFT_SHIFT",
    "KEY_RIGHT_SHIFT",
    "KEY_LEFT_CONTROL",
    "KEY_RIGHT_CONTROL",
    "KEY_LEFT_ALT",
    "KEY_RIGHT_ALT",
    "KEY_LEFT_SUPER",
    "KEY_RIGHT_SUPER",
    "KEY_MENU",
    "KEY_KP_0",
    "KEY_KP_1",
    "KEY_KP_2",
    "KEY_KP_3",
    "KEY_KP_4",
    "KEY_KP_5",
    "KEY_KP_6",
    "KEY_KP_7",
    "KEY_KP_8",
    "KEY_KP_9",
    "KEY_KP_DECIMAL",
    "KEY_KP_DIVIDE",
    "KEY_KP_MULTIPLY",
    "KEY_KP_SUBTRACT",
    "KEY_KP_ADD",
    "KEY_KP_ENTER",
    "KEY_KP_EQUAL",
]
