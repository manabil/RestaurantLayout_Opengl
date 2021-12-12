import glfw
import pyrr
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

    layout(location = 0) in vec3 position_in;
    layout(location = 1) in vec3 color_in;
    uniform mat4 rotation;
    out vec3 color_out;

    void main()
    {
        gl_Position = rotation * vec4(position_in, 1.0);
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
vertices = [-0.5, -0.5, 0.025,    1.0, 0.0, 0.0,
            0.5, -0.5, 0.025,    0.0, 1.0, 0.0,
            0.5,  0.5, 0.025,    0.0, 0.0, 1.0,
            -0.5,  0.5, 0.025,    1.0, 1.0, 1.0,

            -0.5, -0.5, -0.025,   1.0, 0.0, 0.0,
            0.5, -0.5, -0.025,   0.0, 1.0, 0.0,
            0.5,  0.5, -0.025,   0.0, 0.0, 1.0,
            -0.5,  0.5, -0.025,   0.0, 1.0, 1.0]
vertices = np.array(vertices, dtype=np.float32)


# Define index array vertex
indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           0, 1, 4, 4, 5, 1,
           1, 5, 6, 6, 2, 1,
           2, 3, 6, 6, 7, 3,
           0, 4, 7, 7, 3, 0]
indices = np.array(indices, dtype=np.uint32)

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Make VBO (Vertex Buffer Object)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Make EBO (Element Buffer Object)
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Define Vertex location
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# Define Vertex color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Call rotation in shader
rotation_loc = glGetUniformLocation(shader, "rotation")

# ==========================================
# Loop until the user closes the window
# ==========================================
while not glfw.window_should_close(window):

    # Clear buffer and Poll process events
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the object
    # Rotate in 3-axis
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.7 * glfw.get_time())
    rot_z = pyrr.Matrix44.from_z_rotation(0.9 * glfw.get_time())

    # 3 Method of rotation
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x * rot_y * rot_z)
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y @ rot_z)
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE,
                       pyrr.matrix44.multiply((rot_x * rot_y), rot_z))
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glfw.swap_buffers(window)

glfw.terminate()
