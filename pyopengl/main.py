import pydraw
import Engine

import time
from math import dist


renderer = pydraw.Pydraw(1920, 1080, "Simple OpenGL Renderer", pydraw.FULLSCREEN, pydraw.V_SYNC_OFF, cursor=1)
image = renderer.load_image("image_test.png")  # Specify the path to your image

frame_count = 0
last_time = time.time()
window_size_x, window_size_y = renderer.get_window_size()

image.set_pos((0, 0), (window_size_x / 2, 0), (window_size_x / 2, window_size_y), (0, window_size_y), renderer.get_window_size())
x, y, z = (40, 1, 40)

map_matrix = [[[1 for i in range(z)] for j in range(x)] for k in range(y)]

engine = Engine.Engine(renderer.get_window_size(), map_matrix, render_dist=40, fixed_camera=True)


dt = 0
engine.camera.speed = 100

old_pos = None
old_angleY = None
old_angleX = None
engine.get_ps_vs_point()

while renderer.window_is_open():
    start = time.time()
    current_time = time.time()
    frame_count += 1
    renderer.start_frame()
    # renderer.fill((135, 206, 235))

    start_time = time.time()

    engine.display_polygons(renderer, image)

    mouse_pos = renderer.mouse.get_pos()
    engine.handle_mouse_movement(renderer.set_cursor_position, mouse_pos[0], mouse_pos[1], dt)
    keys = renderer.key.get_pressed()
    if keys[renderer.KEY_SPACE]:
        engine.camera.go_up(dt)
    if keys[renderer.KEY_LEFT_SHIFT]:
        engine.camera.go_down(dt)
    if keys[renderer.KEY_W]:
        engine.camera.go_forward(dt)
    if keys[renderer.KEY_S]:
        engine.camera.go_backward(dt)
    if keys[renderer.KEY_D]:
        engine.camera.go_right(dt)
    if keys[renderer.KEY_A]:
        engine.camera.go_left(dt)



    if current_time - last_time >= 1.0:  # Every second, update the framerate display
        print(f"Framerate: {frame_count} FPS")
        frame_count = 0
        last_time = current_time

    dt = time.time() - current_time
    renderer.end_frame()

    # if time.time() - start < 0.04:
    #     print(time.time() - start)




