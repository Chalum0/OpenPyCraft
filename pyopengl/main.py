import pydraw

import time


# Usage example :
if __name__ == "__main__":
    renderer = pydraw.Pydraw(640, 480, "Simple OpenGL Renderer")
    image = renderer.load_image("image_test.png")  # Specify the path to your image
    image2 = renderer.load_image("image_test.png")  # Specify the path to your image

    frame_count = 0
    last_time = time.time()
    window_size_x, window_size_y = renderer.get_window_size()

    image.set_pos((0, 0), (window_size_x/2, 0), (window_size_x/2, window_size_y), (0, window_size_y), renderer.get_window_size())
    image2.set_pos((window_size_x/2, 0), (window_size_x, 0), (window_size_x, window_size_y), (window_size_x/2, window_size_y), renderer.get_window_size())

    while renderer.window_is_open():
        current_time = time.time()
        frame_count += 1
        renderer.start_frame()

        renderer.draw_image(image)
        renderer.draw_image(image2)

        keys = renderer.key.get_pressed()

        mouse = renderer.mouse.get_pressed()



        if current_time - last_time >= 1.0:  # Every second, update the framerate display
            print(f"Framerate: {frame_count} FPS")
            frame_count = 0
            last_time = current_time
        for event in renderer.get_events():
            if event.type == renderer.KEY_DOWN:

        renderer.end_frame()
