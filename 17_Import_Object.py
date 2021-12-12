import os
import pyrr
import pygame
from OpenGL.GL import *
from OBJ_Loader import ObjLoader
from Texture_Loader import load_texture_pygame
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

# Define Object
sushi_indices, sushi_buffer = ObjLoader.load_model('object/sushi.obj')

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

# Sushi Object 🍣🍣🍣
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
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

# load texture
texture = glGenTextures(1)
sushi_tex = load_texture_pygame('textures/sushi.png', texture)

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(45, 800/600, 0.1, 100)
view = pyrr.matrix44.create_look_at(pyrr.Vector3(
    [0, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
sushi = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -10]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

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

    # Rotation
    # rot_x = pyrr.Matrix44.from_x_rotation(0.7 * counter)
    rot_y = pyrr.Matrix44.from_y_rotation(0.7 * counter)
    rot_z = pyrr.Matrix44.from_z_rotation(0.5 * counter)
    rotation = pyrr.matrix44.multiply(rot_z, rot_y)

    # Draw Object
    model = pyrr.matrix44.multiply(rotation, sushi)
    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, sushi_tex)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    pygame.display.flip()

pygame.quit()
