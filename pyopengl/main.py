import pydraw
import Engine
import threading
import socket
import time
import random
from math import dist
import ast


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

host = "164.132.51.168"
port = 8080
FORMAT = "UTF-8"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
socket.send(f"{random.randint(10000, 99999)}".encode(FORMAT))

got_response = True
poses = []


def get_player_pos(pos):
    global got_response
    global poses
    got_response = False
    socket.send(str(pos).encode(FORMAT))
    poses = socket.recv(1024).decode(FORMAT)
    poses = ast.literal_eval(poses)

    for i_d in poses:
        if i_d in engine.entity_ids:
            engine.entity_ids[i_d].set_pos(poses[i_d])
        else:
            engine.entity_ids[i_d] = Engine.Entity(poses[i_d], engine.block_size/2, i_d)

    engine.get_entities()



    # engine.kill_all_entities()
    # for p in poses:
    #     entity = Engine.Entity(p, engine.block_size / 2, "other")
    #     engine.entities.append(entity)
    # engine.get_entity_polygons()
    got_response = True


def get_networking(player_pos):
    my_thread = threading.Thread(target=get_player_pos, args=(player_pos,))
    my_thread.start()


while renderer.window_is_open():
    start = time.time()
    current_time = time.time()
    frame_count += 1
    renderer.start_frame()
    # renderer.fill((135, 206, 235))

    if got_response:
        get_networking(engine.camera.player.pos)

    start_time = time.time()

    engine.display_polygons(renderer, image)

    mouse_pos = renderer.mouse.get_pos()
    engine.handle_mouse_movement(renderer.set_cursor_position, mouse_pos[0], mouse_pos[1], dt)
    keys = renderer.key.get_pressed()
    if keys[renderer.KEY_SPACE]:
        engine.camera.go_up(dt)
    if keys[renderer.KEY_LEFT_SHIFT]:
        engine.camera.go_down(dt)
    if keys[renderer.KEY_D]:
        engine.camera.go_forward(dt)
    if keys[renderer.KEY_A]:
        engine.camera.go_backward(dt)
    if keys[renderer.KEY_S]:
        engine.camera.go_right(dt)
    if keys[renderer.KEY_W]:
        engine.camera.go_left(dt)



    if current_time - last_time >= 1.0:  # Every second, update the framerate display
        print(f"Framerate: {frame_count} FPS")
        frame_count = 0
        last_time = current_time

    dt = time.time() - current_time
    renderer.end_frame()

socket.send("quit".encode(FORMAT))
socket.close()
