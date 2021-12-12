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
    layout(location = 3) in vec3 color_in;
    
    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;
    

    out vec2 texture_out;
    out vec3 color_out;

    void main()
    {
        gl_Position = projection * view * model * (vec4(position_in, 1.0));
        texture_out = texture_in;
        color_out = color_in;
    }
"""
fragment_src = """
    # version 330

    in vec2 texture_out;
    in vec3 color_out;

    uniform sampler2D texture_sampler;
    uniform int switcher;
    uniform vec3 objectColor;
    uniform vec3 lightColor;

    out vec4 color;

    void main()
    {
        if(switcher == 0){
            color = texture(texture_sampler, texture_out);
        }
        else{
            color = vec4(lightColor * objectColor, 1.0);
        }
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
cube_vertices = [-0.5, -0.5,  0.5,   1, 1, 1,
                 0.5, -0.5,  0.5,    1, 1, 1,
                 0.5,  0.5,  0.5,    1, 1, 1,
                 -0.5,  0.5,  0.5,   1, 1, 1,

                 -0.5, -0.5, -0.5,   1, 1, 1,
                 0.5, -0.5, -0.5,    1, 1, 1,
                 0.5,  0.5, -0.5,    1, 1, 1,
                 -0.5,  0.5, -0.5,   1, 1, 1,

                 0.5, -0.5, -0.5,    1, 1, 1,
                 0.5,  0.5, -0.5,    1, 1, 1,
                 0.5,  0.5,  0.5,    1, 1, 1,
                 0.5, -0.5,  0.5,    1, 1, 1,

                 -0.5, -0.5, -0.5,   1, 1, 1,
                 -0.5,  0.5, -0.5,   1, 1, 1,
                 -0.5,  0.5,  0.5,   1, 1, 1,
                 -0.5, -0.5,  0.5,   1, 1, 1,

                 -0.5, -0.5, -0.5,   1, 1, 1,
                 0.5, -0.5, -0.5,    1, 1, 1,
                 0.5, -0.5,  0.5,    1, 1, 1,
                 -0.5, -0.5,  0.5,   1, 1, 1,

                 -0.5,  0.5, -0.5,   1, 1, 1,
                 0.5,  0.5, -0.5,    1, 1, 1,
                 0.5,  0.5,  0.5,    1, 1, 1,
                 -0.5,  0.5,  0.5,   1, 1, 1]
cube_vertices = np.array(cube_vertices, dtype=np.float32)
cube_indices = [0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]
cube_indices = np.array(cube_indices, dtype=np.uint32)

sushi_indices, sushi_buffer = ObjLoader.load_model('object/sushi.obj')
floor_indices, floor_buffer = ObjLoader.load_model('object/floor.obj')

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(3)
VBO = glGenBuffers(3)
EBO = glGenBuffers(1)

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

# Floor Object 🟫🟫🟫
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
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

# Light Object
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, cube_vertices.nbytes,
             cube_vertices, GL_STATIC_DRAW)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes,
             cube_indices, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      cube_vertices.itemsize * 6, ctypes.c_void_p(0))
glEnableVertexAttribArray(3)
glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE,
                      cube_vertices.itemsize * 6, ctypes.c_void_p(12))

# load texture
texture = glGenTextures(3)
load_texture_pygame('textures/sushi.png', texture[0])
load_texture_pygame('textures/floor.png', texture[1])
load_texture_pygame('textures/wood.jpeg', texture[2])

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(
    45, WIDTH/HEIGHT, 0.1, 100)
sushilb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([0, 2, 0]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
cube = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 10, 0]))

glEnable(GL_LIGHTING)


model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
switcher_loc = glGetUniformLocation(shader, "switcher")

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
    glUniform1i(switcher_loc, 0)

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
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sushilb_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Floor 🟫
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # Draw Cube🟫
    glBindVertexArray(VAO[2])
    glUniform1i(switcher_loc, 1)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube)
    glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)

    pygame.display.flip()

pygame.quit()
