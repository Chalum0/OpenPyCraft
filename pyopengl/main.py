import pydraw
import Engine

import time


# Usage example :
if __name__ == "__main__":
    renderer = pydraw.Pydraw(640, 480, "Simple OpenGL Renderer", pydraw.FULLSCREEN, pydraw.V_SYNC_OFF, cursor=1)
    image = renderer.load_image("image_test.png")  # Specify the path to your image

    frame_count = 0
    last_time = time.time()
    window_size_x, window_size_y = renderer.get_window_size()

    image.set_pos((0, 0), (window_size_x / 2, 0), (window_size_x / 2, window_size_y), (0, window_size_y), renderer.get_window_size())

    engine = Engine.Engine(renderer.get_window_size())

    for x in range(1):
        for z in range(1):
            engine.create_block((10*x, 0, 10*z), 5)

    engine.optimise_points()

    dt = 0
    engine.camera.speed = 100

    while renderer.window_is_open():
        current_time = time.time()
        frame_count += 1
        renderer.start_frame()

        start_time = time.time()
        engine.get_ps_vs_point()
        # print(time.time() - start_time)

        if len(engine.points) >= 2:
            # print(len(engine.polygons))
            for k in engine.polygons:
                i = k.get_points()
                # print(i)
                not_false_point = []
                len_points = 0
                points = []
                pts = []
                start_time = time.time()
                for y in range(len(i)):
                    point = i[y]
                    # print(point, i)
                    ps_point = point.ps
                    points.append(ps_point)
                    len_points += 1
                    pts.append(point.vs_point)
                    if ps_point is not None:
                        not_false_point.append(ps_point)
                if len(not_false_point) >= 1:
                    if None in points:
                        pass
                    else:
                        image.set_pos(points[0], points[1], points[2], points[3], renderer.get_window_size())
                        print(points[0], points[1], points[2], points[3])
                        renderer.draw_image(image)
                # print(time.time() - start_time)

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
