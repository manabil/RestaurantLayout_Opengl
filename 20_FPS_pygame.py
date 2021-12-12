import os
import pyrr
import pygame
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
    layout(location = 2) in vec3 normal_in;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;

    out vec3 color_out;
    out vec2 texture_out;

    void main()
    {
        gl_Position = projection * view * model * vec4(position_in, 1.0);
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
sushi_indices, sushi_buffer = ObjLoader.load_model('object/sushi.obj')
plate_indices, plate_buffer = ObjLoader.load_model('object/plate.obj')
other_indices, other_buffer = ObjLoader.load_model('object/table2.obj')
other2_indices, other2_buffer = ObjLoader.load_model('object/pot.obj')
floor_indices, floor_buffer = ObjLoader.load_model('object/floor.obj')

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(5)
VBO = glGenBuffers(5)

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

# Wooden Plate Object 🧫🧫🧫
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, plate_buffer.nbytes,
             plate_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      plate_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      plate_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      plate_buffer.itemsize * 8, ctypes.c_void_p(20))

# Other Object ✨✨✨
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, other_buffer.nbytes,
             other_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      other_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      other_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      other_buffer.itemsize * 8, ctypes.c_void_p(20))

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

# Other2 Object ✨✨✨
glBindVertexArray(VAO[4])
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, other2_buffer.nbytes,
             other2_buffer, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      other2_buffer.itemsize * 8, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      other2_buffer.itemsize * 8, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      other2_buffer.itemsize * 8, ctypes.c_void_p(20))

# load texture
texture = glGenTextures(4)
load_texture_pygame('textures/sushi.png', texture[0])
load_texture_pygame('textures/mahogany.png', texture[1])
load_texture_pygame('textures/floor.jpg', texture[2])
load_texture_pygame('textures/pot.jpeg', texture[3])

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(
    45, WIDTH/HEIGHT, 0.1, 100)
sushi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 4, 0]))
# plate_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 4, 0]))
other_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 0, 15]))
other2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, 15]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

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

    # Rotation
    rot_x = pyrr.Matrix44.from_x_rotation(0.7 * counter)
    rot_y = pyrr.Matrix44.from_y_rotation(0.7 * counter)
    rot_z = pyrr.Matrix44.from_z_rotation(0.5 * counter)
    rotation = pyrr.matrix44.multiply(rot_z, rot_y)

    # Draw Sushi 🍣
    model = pyrr.matrix44.multiply(rotation, sushi_pos)
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Plate 🧫
    plate_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3(
        [-10 + (5 * sin(counter*1.5)), 3, 0]))
    glBindVertexArray(VAO[1])
    rot_z = pyrr.Matrix44.from_z_rotation(2.5 * counter)
    model = pyrr.matrix44.multiply(rot_z, plate_pos)
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Other ✨
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, other_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(other_indices))

    # Draw Other2 ✨
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, texture[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, other2_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(other2_indices))

    # Draw Floor 🟫
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, texture[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    pygame.display.flip()

pygame.quit()
