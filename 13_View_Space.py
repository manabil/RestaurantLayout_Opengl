import os
import math
import pyrr
import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# ==========================================
# Vertex and fragment shader
# ==========================================
vertex_src = """
    # version 330

    layout(location = 0) in vec3 position_in;
    layout(location = 1) in vec2 texture_in;

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


# =============================================
# Define vertices ,color and index vertex array
# =============================================
vertices = [-0.5, -0.5,  0.5,   0.0, 0.0,
            0.5, -0.5,  0.5,    1.0, 0.0,
            0.5,  0.5,  0.5,    1.0, 1.0,
            -0.5,  0.5,  0.5,   0.0, 1.0,

            -0.5, -0.5, -0.5,   0.0, 0.0,
            0.5, -0.5, -0.5,    1.0, 0.0,
            0.5,  0.5, -0.5,    1.0, 1.0,
            -0.5,  0.5, -0.5,   0.0, 1.0,

            0.5, -0.5, -0.5,  0.0, 0.0,
            0.5,  0.5, -0.5,  1.0, 0.0,
            0.5,  0.5,  0.5,  1.0, 1.0,
            0.5, -0.5,  0.5,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0,

            -0.5, -0.5, -0.5,   0.0, 0.0,
            0.5, -0.5, -0.5,    1.0, 0.0,
            0.5, -0.5,  0.5,    1.0, 1.0,
            -0.5, -0.5,  0.5,   0.0, 1.0,

            -0.5,  0.5, -0.5,   1.0, 0.0,
            0.5,  0.5, -0.5,    0.0, 0.0,
            0.5,  0.5,  0.5,    0.0, 1.0,
            -0.5,  0.5,  0.5,   1.0, 1.0]
vertices = np.array(vertices, dtype=np.float32)

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
           12, 13, 14, 14, 15, 12,
           16, 17, 18, 18, 19, 16,
           20, 21, 22, 22, 23, 20]
indices = np.array(indices, dtype=np.uint32)

# Window init
pygame.init()
pygame.display.set_mode((640, 480), pygame.OPENGL |
                        pygame.DOUBLEBUF | pygame.RESIZABLE)
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Make VBO (Vertex Buffer Object) , EBO (Element Buffer Object) & Texture Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      vertices.itemsize * 5, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      vertices.itemsize * 5, ctypes.c_void_p(12))

# Set the texture wrapping and filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# load image
image = pygame.image.load('textures/wood.jpeg')
image = pygame.transform.flip(image, False, False)
image_width, image_height = image.get_rect().size
img_data = pygame.image.tostring(image, 'RGBA')
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
             image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(45, 640/480, 0.1, 100)
translation = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([0, 0, 0]))
# view = pyrr.matrix44.create_from_translation(
#     pyrr.Vector3([-1, 0, 0]))
# view = pyrr.matrix44.create_look_at(pyrr.Vector3(
#     [2, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(model_loc, 1, GL_FALSE, translation)
# glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

running = True

# ==========================================
# Loop until the user closes the window
# ==========================================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
            projection = pyrr.matrix44.create_perspective_projection(
                45, event.w/event.h, 0.1, 100)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    counter = pygame.time.get_ticks() / 1000

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camX = math.sin(counter) * 3
    camZ = math.cos(counter) * 3
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([camX, 1.5, camZ]), pyrr.Vector3([0.0, 0.0, 0.0]),
                                        pyrr.Vector3([0.0, 1.0, 0.0]))

    # 3 Method of rotation
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    pygame.display.flip()

pygame.quit()
