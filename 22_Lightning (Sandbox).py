import os
import pyrr
import pygame
import numpy as np
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
    layout(location = 2) in vec3 normal_in;
    
    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;
    uniform mat4 scale;
    uniform mat4 rotate;

    out vec2 texture_out;

    void main()
    {
        gl_Position = projection * view * model * (vec4(position_in, 1.0) * scale * rotate);
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
        cam.process_keyboard("LEFT", 0.25)
    if keys_pressed[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.25)
    if keys_pressed[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.25)
    if keys_pressed[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.25)
    if keys_pressed[pygame.K_z]:
        cam.process_keyboard("UP", 0.25)
    if keys_pressed[pygame.K_x]:
        cam.process_keyboard("DOWN", 0.25)
    if keys_pressed[pygame.K_q]:
        cam.process_keyboard("YAWL", 0.25)
    if keys_pressed[pygame.K_e]:
        cam.process_keyboard("YAWR", 0.25)


# Window init
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL |
                        pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption('Kelompok 5 - Restaurant')
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


# =============================================
# Define Object, Shader, VBO, EBO, and VAO
# =============================================

# Define Object
sushi_indices, sushi_buffer = ObjLoader.load_model('object/sushi.obj')
plate_indices, plate_buffer = ObjLoader.load_model('object/plate.obj')
table_indices, table_buffer = ObjLoader.load_model('object/table.obj')
pot_indices, pot_buffer = ObjLoader.load_model('object/pot.obj')
floor_indices, floor_buffer = ObjLoader.load_model('object/floor.obj')
chair_indices, chair_buffer = ObjLoader.load_model('object/chair.obj')
wallSide_indices, wallSide_buffer = ObjLoader.load_model(
    'object/wall_side.obj')
wallBack_indices, wallBack_buffer = ObjLoader.load_model(
    'object/wall_back.obj')

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(7)
VBO = glGenBuffers(7)

# Sushi Object 🍣🍣🍣
glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, sushi_buffer.nbytes,
             sushi_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      sushi_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      sushi_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      sushi_buffer.itemsize * 8, ctypes.c_void_p(20))

# Wooden Wall Side
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, wallSide_buffer.nbytes,
             wallSide_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      wallSide_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      wallSide_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      wallSide_buffer.itemsize * 8, ctypes.c_void_p(20))

# Table Object ✨✨✨
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, table_buffer.nbytes,
             table_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      table_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      table_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      table_buffer.itemsize * 8, ctypes.c_void_p(20))

# Floor Object 🟫🟫🟫
glBindVertexArray(VAO[3])
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes,
             floor_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      floor_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      floor_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      floor_buffer.itemsize * 8, ctypes.c_void_p(20))

# Pot Object ✨✨✨
glBindVertexArray(VAO[4])
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, pot_buffer.nbytes, pot_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      pot_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      pot_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      pot_buffer.itemsize * 8, ctypes.c_void_p(20))

# Chair Object ✨✨✨
glBindVertexArray(VAO[5])
glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
glBufferData(GL_ARRAY_BUFFER, chair_buffer.nbytes,
             chair_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      chair_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      chair_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      chair_buffer.itemsize * 8, ctypes.c_void_p(20))

# Wooden Wall Back
glBindVertexArray(VAO[6])
glBindBuffer(GL_ARRAY_BUFFER, VBO[6])
glBufferData(GL_ARRAY_BUFFER, wallBack_buffer.nbytes,
             wallBack_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      wallBack_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      wallBack_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      wallBack_buffer.itemsize * 8, ctypes.c_void_p(20))

# load texture
texture = glGenTextures(7)
load_texture_pygame('textures/sushi.png', texture[0])
load_texture_pygame('textures/mahogany.png', texture[1])
load_texture_pygame('textures/floor.png', texture[2])
load_texture_pygame('textures/pot.jpeg', texture[3])
load_texture_pygame('textures/chair.png', texture[4])
load_texture_pygame('textures/plafon.jpg', texture[5])
load_texture_pygame('textures/wall_side.jpg', texture[6])

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(
    45, WIDTH/HEIGHT, 0.1, 100)
# Table Position
tablerf_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, -10]))
tablelf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, -10]))
tablelb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-30, 0, 15]))
tablemf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, -10]))
tablemb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 0, 15]))
tablerb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, 15]))
# Sushi Position
sushirf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 4.8, -10]))
sushilf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 4.8, -10]))
sushilb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 4.8, 15]))
sushimf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 4.8, -10]))
sushimb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 4.8, 15]))
sushirb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 4.8, 15]))
# Chair 1 Position
chair1rf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, -15]))
chair1lf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, -15]))
chair1lb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, 10]))
chair1mf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, -15]))
chair1mb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, 10]))
chair1rb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, 10]))
# Chair 2 Position
chair2rf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, -3]))
chair2mf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, -3]))
chair2lf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, -3]))
chair2lb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, 22]))
chair2mb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, 22]))
chair2rb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, 22]))
# Pot Position
potlb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-40, 0, 23]))
potlf_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-40, 0, -23]))
potmlb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-20, 0, 23]))
potmlf_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-20, 0, -23]))
potmrb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 23]))
potmrf_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -23]))
potrb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([20, 0, 23]))
potrf_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([20, 0, -23]))
# Wall, Roof , Floor Position
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
roof_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 20, 0]))
wallSideR_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([25, 0, 0]))
wallSideL_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-45, 0, 0]))
wallBack_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -26]))

rotate = pyrr.matrix44.create_from_y_rotation(30)
no_rotate = pyrr.matrix44.create_from_y_rotation(0)

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
scale_loc = glGetUniformLocation(shader, "scale")
rotate_loc = glGetUniformLocation(shader, "rotate")

table_scl = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.7, 0.7, 0.7]))
sushi_scl = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.2, 0.2, 0.2]))
chair_scl = pyrr.matrix44.create_from_scale(pyrr.Vector3([2.5, 2.5, 2.5]))
pot_scl = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.7, 0.7, 0.7]))
floor_scl = pyrr.matrix44.create_from_scale(pyrr.Vector3([1, 1, 1]))

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

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

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Movement key
    key_press()
    mouse_pos = pygame.mouse.get_pos()
    mouse_look(mouse_pos[0], mouse_pos[1])

    # 360° Look Around
    if mouse_pos[0] <= 0:
        cam.process_keyboard("YAWL", 0.25)
    elif mouse_pos[0] >= WIDTH-1:
        cam.process_keyboard("YAWR", 0.25)

    # View Matrix
    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # Draw Sushi ✨
    # Left Back
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushilb_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, sushi_scl)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))
    # Right Back
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushirb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))
    # Middle Back
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushimb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))
    # Left Front
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushilf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))
    # Right Front
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushirf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))
    # Middle Front
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushimf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Table ✨
    # Left Back
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablelb_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, table_scl)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))
    # Right Back
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablerb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))
    # Middle Back
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablemb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))
    # Left Front
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablelf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))
    # Right Front
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablerf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))
    # Middle Front
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tablemf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(table_indices))

    # Draw Pot ✨
    #  left Back
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potlb_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, pot_scl)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    #  left Front
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potlf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Middle left Back
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potmlb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Middle left Front
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potmlf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Middle Right Back
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potmrb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Middle Right Front
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potmrf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Right Back
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potrb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))
    # Right Front
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, potrf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pot_indices))

    # Draw Chair ✨
    # Chair 1
    # Left Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1lb_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, chair_scl)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Right Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1rb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Middle Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1mb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Left Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1lf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Right Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1rf_pos)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Middle Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair1mf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Chair 2
    # Left Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2lb_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, chair_scl)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Right Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2rb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Middle Back
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2mb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Left Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2lf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Right Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2rf_pos)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))
    # Middle Front
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, texture[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, chair2mf_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(chair_indices))

    # Draw Floor 🟫
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, floor_scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, no_rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # Draw Roof
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, texture[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, roof_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, floor_scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, no_rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # Draw Wall
    # Wall side Right
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, texture[6])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, wallSideR_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, floor_scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, no_rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(wallSide_indices))
    # Wall side Left
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, texture[6])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, wallSideL_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, floor_scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, no_rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(wallSide_indices))
    # Wall back
    glBindVertexArray(VAO[6])
    glBindTexture(GL_TEXTURE_2D, texture[6])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, wallBack_pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, floor_scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, no_rotate)
    glDrawArrays(GL_TRIANGLES, 0, len(wallBack_indices))

    pygame.display.flip()

pygame.quit()
