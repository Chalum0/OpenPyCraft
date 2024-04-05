import pydraw
import Engine

import time

if __name__ == "__main__":
    renderer = pydraw.Pydraw(640, 480, "Simple OpenGL Renderer", pydraw.FULLSCREEN, pydraw.V_SYNC_OFF, cursor=1)
    image = renderer.load_image("image_test.png")  # Specify the path to your image

    frame_count = 0
    last_time = time.time()
    window_size_x, window_size_y = renderer.get_window_size()

    image.set_pos((0, 0), (window_size_x / 2, 0), (window_size_x / 2, window_size_y), (0, window_size_y), renderer.get_window_size())

    dt = 0

    while renderer.window_is_open():
        current_time = time.time()
        frame_count += 1
        renderer.start_frame()

        start_time = time.time()

        image.set_pos([749.7374867503944, 415.3486786438741], [613.9099249756276, 421.13206190488063], [660.3744414278642, 638.9624535007106], [788.6450518852187, 716.6518323850571], renderer.get_window_size())
        renderer.draw_image(image)

        if current_time - last_time >= 1.0:  # Every second, update the framerate display
            print(f"Framerate: {frame_count} FPS")
            frame_count = 0
            last_time = current_time

        dt = time.time() - current_time
        renderer.end_frame()
