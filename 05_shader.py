import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# ==========================================
# Vertex and fragment shader
# ==========================================
vertex_src = """
    # version 330

    in vec3 position_in;
    in vec3 color_in;
    out vec3 color_out;

    void main()
    {
        gl_Position = vec4(position_in, 1.0);
        color_out = color_in;
    }
"""

fragment_src = """
    # version 330

    in vec3 color_out;
    out vec4 color;

    void main()
    {
        color = vec4(color_out, 1.0);
    }
"""

# ==========================================
# Initialize window & context
# ==========================================
if not glfw.init():
    raise Exception('glfw can\'t be initialized')

# creating the window
window = glfw.create_window(640, 480, "Kelompok 5 - Sushi", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception('glfw window can\'t be created')

# set window's position
glfw.set_window_pos(window, 100, 100)

# Get callback and windows resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)


# ==========================================
# Define vertices and color
# ==========================================
vertices = [0, 0.5, 0,          1, 0, 0,
            - 0.5, -0.5, 0,     0, 1, 0,
            0.5, -0.5, 0,       0, 0, 1]
vertices = np.array(vertices, dtype=np.float32)

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Make Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Define Vertex location
position = glGetAttribLocation(shader, "position_in")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# Define color
color = glGetAttribLocation(shader, "color_in")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)


# ==========================================
# Loop until the user closes the window
# ==========================================
while not glfw.window_should_close(window):

    # Clear buffer and Poll process events
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the object
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glfw.swap_buffers(window)

glfw.terminate()
