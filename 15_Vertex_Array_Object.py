import os
import math
import pyrr
import pygame
import numpy as np
from OpenGL.GL import *
from libraries.Texture_Loader import load_texture_pygame
from OpenGL.GL.shaders import compileProgram, compileShader

# ==========================================
# Vertex and fragment shader
# ==========================================
vertex_src = """
    # version 330

    layout(location = 0) in vec3 position_in;
    layout(location = 1) in vec2 texture_in;
    layout(location = 2) in vec3 color_in;

    uniform mat4 model;
    uniform mat4 projection;
    uniform mat4 view;

    out vec3 color_out;
    out vec2 texture_out;

    void main()
    {
        gl_Position = projection * view * model * vec4(position_in, 1.0);
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

    out vec4 color;

    void main()
    {
        if(switcher == 0){
            color = texture(texture_sampler, texture_out);
        }
        else{
            color = vec4(color_out, 1.0);
        }
    }
"""

# =============================================
# Define vertices ,color and index vertex array
# =============================================
# Cube Object
cube_vertices = [-0.5, -0.5,  0.5,   0.0, 0.0,
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
cube_vertices = np.array(cube_vertices, dtype=np.float32)
cube_indices = [0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]
cube_indices = np.array(cube_indices, dtype=np.uint32)

# Quad Object
quad_vertices = [-0.5, -0.5, 0, 0.0, 0.0,
                 0.5, -0.5, 0, 1.0, 0.0,
                 0.5,  0.5, 0, 1.0, 1.0,
                 -0.5,  0.5, 0, 0.0, 1.0]
quad_vertices = np.array(quad_vertices, dtype=np.float32)
quad_indices = [0, 1, 2, 2, 3, 0]
quad_indices = np.array(quad_indices, dtype=np.uint32)

# Triangle Object
triangle_vertices = [-0.5, -0.5, 0, 1, 0, 0,
                     0.5, -0.5, 0, 0, 1, 0,
                     0.0,  0.5, 0, 0, 0, 1]
triangle_vertices = np.array(triangle_vertices, dtype=np.float32)

# Window init
pygame.init()
pygame.display.set_mode((640, 480), pygame.OPENGL |
                        pygame.DOUBLEBUF | pygame.RESIZABLE)
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))


# =============================================
# Define VBO, EBO, and VAO
# =============================================

# Cube Object 🧊
cube_VAO = glGenVertexArrays(1)
glBindVertexArray(cube_VAO)
cube_VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, cube_VBO)
glBufferData(GL_ARRAY_BUFFER, cube_vertices.nbytes,
             cube_vertices, GL_STATIC_DRAW)
cube_EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes,
             cube_indices, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      cube_vertices.itemsize * 5, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      cube_vertices.itemsize * 5, ctypes.c_void_p(12))

# QUAD OBJECT ⬜
quad_VAO = glGenVertexArrays(1)
glBindVertexArray(quad_VAO)
quad_VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, quad_VBO)
glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes,
             quad_vertices, GL_STATIC_DRAW)
quad_EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, quad_EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad_indices.nbytes,
             quad_indices, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      quad_vertices.itemsize * 5, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      quad_vertices.itemsize * 5, ctypes.c_void_p(12))

# TRIANGLE OBJECT 🔺
triangle_VAO = glGenVertexArrays(1)
glBindVertexArray(triangle_VAO)
triangle_VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, triangle_VBO)
glBufferData(GL_ARRAY_BUFFER, triangle_vertices.nbytes,
             triangle_vertices, GL_STATIC_DRAW)
# Define Vertex and Texture Shader
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      triangle_vertices.itemsize * 6, ctypes.c_void_p(0))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                      triangle_vertices.itemsize * 6, ctypes.c_void_p(12))

# load texture
texture = glGenTextures(2)
cube_tex = load_texture_pygame('textures/wood.jpeg', texture[0])
quad_tex = load_texture_pygame('textures/brick.png', texture[1])

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(45, 800/600, 0.1, 100)
view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
cube = pyrr.matrix44.create_from_translation(pyrr.Vector3([1, 0, 0]))
quad = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1, 0, 0]))
triangle = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 1, -1]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
switcher_loc = glGetUniformLocation(shader, "switcher")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

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
    glUniform1i(switcher_loc, 0)

    # Rotation
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * counter)
    rot_y = pyrr.Matrix44.from_y_rotation(0.7 * counter)
    rot_z = pyrr.Matrix44.from_z_rotation(0.9 * counter)
    rotation = pyrr.matrix44.multiply((rot_x * rot_y), rot_z)

    # Draw Object
    model = pyrr.matrix44.multiply(rotation, cube)
    glBindVertexArray(cube_VAO)
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)

    model = pyrr.matrix44.multiply(rot_x, quad)
    glBindVertexArray(quad_VAO)
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)

    model = pyrr.matrix44.multiply(rot_y, triangle)
    glBindVertexArray(triangle_VAO)
    glUniform1i(switcher_loc, 1)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    pygame.display.flip()

pygame.quit()
