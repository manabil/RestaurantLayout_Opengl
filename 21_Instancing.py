import os
import pyrr
import pygame
import numpy as np
from math import sin
from OpenGL.GL import *
from libraries.Camera import Camera
from libraries.OBJ_Loader import ObjLoader
from libraries.Texture_Loader import load_texture_pygame
from OpenGL.GL.shaders import compileProgram, compileShader

# ==========================================
# Vertex and fragment shader
# ==========================================
vertex_src = """
    # version 330

    layout(location = 0) in vec3 position_in;
    layout(location = 1) in vec2 texture_in;
    layout(location = 2) in vec3 offset_in;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;

    out vec2 texture_out;

    void main()
    {
        vec3 final_pos = position_in + offset_in;
        gl_Position = projection * view * model * vec4(final_pos, 1.0);
        texture_out = texture_in;
    }
"""
fragment_src = """
    # version 330

    in vec2 texture_out;
    
    uniform sampler2D texture_sampler;

    out vec4 color;

    void main()
    {
        color = texture(texture_sampler, texture_out);
    }
"""

# Camera settings
cam = Camera()
WIDTH, HEIGHT = 640, 480
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


def mouse_look(xpos, ypos):
    # FPS Mouse Camera
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


def key_press():
    # WASD Movement
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        cam.process_keyboard("LEFT", 0.05)
    if keys_pressed[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.05)
    if keys_pressed[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.05)
    if keys_pressed[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.05)
    if keys_pressed[pygame.K_z]:
        cam.process_keyboard("UP", 0.05)
    if keys_pressed[pygame.K_x]:
        cam.process_keyboard("DOWN", 0.05)
    if keys_pressed[pygame.K_q]:
        cam.process_keyboard("YAWL", 0.05)
    if keys_pressed[pygame.K_e]:
        cam.process_keyboard("YAWR", 0.05)


# Window init
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL |
                        pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption('Kelompok 5 - Sushi')
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


# =============================================
# Define Object, Shader, VBO, EBO, and VAO
# =============================================

# Define Object
cube_buffer = [-0.5, -0.5,  0.5, 0.0, 0.0,
               0.5, -0.5,  0.5, 1.0, 0.0,
               0.5,  0.5,  0.5, 1.0, 1.0,
               -0.5,  0.5,  0.5, 0.0, 1.0,

               -0.5, -0.5, -0.5, 0.0, 0.0,
               0.5, -0.5, -0.5, 1.0, 0.0,
               0.5,  0.5, -0.5, 1.0, 1.0,
               -0.5,  0.5, -0.5, 0.0, 1.0,

               0.5, -0.5, -0.5, 0.0, 0.0,
               0.5,  0.5, -0.5, 1.0, 0.0,
               0.5,  0.5,  0.5, 1.0, 1.0,
               0.5, -0.5,  0.5, 0.0, 1.0,

               -0.5,  0.5, -0.5, 0.0, 0.0,
               -0.5, -0.5, -0.5, 1.0, 0.0,
               -0.5, -0.5,  0.5, 1.0, 1.0,
               -0.5,  0.5,  0.5, 0.0, 1.0,

               -0.5, -0.5, -0.5, 0.0, 0.0,
               0.5, -0.5, -0.5, 1.0, 0.0,
               0.5, -0.5,  0.5, 1.0, 1.0,
               -0.5, -0.5,  0.5, 0.0, 1.0,

               0.5,  0.5, -0.5, 0.0, 0.0,
               -0.5,  0.5, -0.5, 1.0, 0.0,
               -0.5,  0.5,  0.5, 1.0, 1.0,
               0.5,  0.5,  0.5, 0.0, 1.0]

cube_indices = [0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

cube_buffer = np.array(cube_buffer, dtype=np.float32)
cube_indices = np.array(cube_indices, dtype=np.uint32)

floor_indices, floor_buffer = ObjLoader.load_model('object/floor.obj')

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
VBO_instance = glGenBuffers(1)
EBO = glGenBuffers(1)

# Cube Object 🧊🧊
glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, EBO)
glBufferData(GL_ARRAY_BUFFER, cube_indices.nbytes,
             cube_indices, GL_STATIC_DRAW)

# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      cube_buffer.itemsize * 5, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      cube_buffer.itemsize * 5, ctypes.c_void_p(12))

# load texture
texture = glGenTextures(1)
load_texture_pygame('textures/stone.png', texture)

# instance VBO
instance_array = []
offset = 1

for z in range(0, 100, 2):
    for y in range(0, 100, 2):
        for x in range(0, 100, 2):
            translation = pyrr.Vector3([0.0, 0.0, 0.0])
            translation.x = x + offset
            translation.y = y + offset
            translation.z = z + offset
            instance_array.append(translation)

# do this before you flatten the array
len_of_instance_array = len(instance_array)
instance_array = np.array(instance_array, np.float32).flatten()

instanceVBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
glBufferData(GL_ARRAY_BUFFER, instance_array.nbytes,
             instance_array, GL_STATIC_DRAW)

glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
# 1 means, every instance will have it's own translate
glVertexAttribDivisor(2, 1)

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(
    45, WIDTH/HEIGHT, 0.1, 100)
cube_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-50, -50, -200]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube_pos)

running = True

# ==========================================
# Loop until the user closes the window
# ==========================================
while running:
    # Event for close and resize window
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
            projection = pyrr.matrix44.create_perspective_projection(
                45, event.w/event.h, 0.1, 100)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    # Movement key
    key_press()
    mouse_pos = pygame.mouse.get_pos()
    mouse_look(mouse_pos[0], mouse_pos[1])

    # 360° Look Around
    if mouse_pos[0] <= 0:
        cam.process_keyboard("YAWL", 0.05)
    elif mouse_pos[0] >= WIDTH-1:
        cam.process_keyboard("YAWR", 0.05)

    # Counter
    counter = pygame.time.get_ticks() / 1000
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # View Matrix
    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # Draw Cube
    glDrawElementsInstanced(GL_TRIANGLES, len(
        cube_indices), GL_UNSIGNED_INT, None, len_of_instance_array)

    pygame.display.flip()

pygame.quit()
