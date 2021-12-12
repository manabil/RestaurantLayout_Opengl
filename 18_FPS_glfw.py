import pyrr
import glfw
from OpenGL.GL import *
from libraries.Camera import Camera
from libraries.OBJ_Loader import ObjLoader
from libraries.Texture_Loader import load_texture
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

# =============================================
# Define Functions
# =============================================

# Camera Initialization
cam = Camera()
WIDTH, HEIGHT = 640, 480
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


def key_input_clb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def mouse_look_clb(window, xpos, ypos):
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


def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# =============================================
# Window and Initialization
# =============================================
if not glfw.init():
    raise Exception("glfw can not be initialized!")
window = glfw.create_window(WIDTH, HEIGHT, "Kelompok 5 - Sushi", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")
glfw.set_window_pos(window, 200, 50)

# Set Callback
glfw.set_window_size_callback(window, window_resize)
glfw.set_cursor_pos_callback(window, mouse_look_clb)
glfw.set_key_callback(window, key_input_clb)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.make_context_current(window)

# =============================================
# Define Object, VBO, EBO, and VAO
# =============================================

# Define Object
sushi_indices, sushi_buffer = ObjLoader.load_model('object/sushi.obj')
plate_indices, plate_buffer = ObjLoader.load_model('object/plate.obj')
floor_indices, floor_buffer = ObjLoader.load_model('object/floor.obj')

# Make Shader Program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(3)
VBO = glGenBuffers(3)

# Sushi Object 🍣
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

# Wooden Plate Object 🧫
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

# Floor Object 🟫
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
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

# load texture
texture = glGenTextures(2)
load_texture('textures/sushi.png', texture[0])
load_texture('textures/floor.jpg', texture[1])

# Using program shader
glUseProgram(shader)
glClearColor(0, 0, 0.1, 0)
glEnable(GL_DEPTH_TEST)

# Define projection, transform, and view array
projection = pyrr.matrix44.create_perspective_projection(
    45, WIDTH/HEIGHT, 0.1, 100)
sushi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 4, 0]))
plate_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 4, 0]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# ==========================================
# Loop until the user closes the window
# ==========================================
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # Rotation
    # rot_x = pyrr.Matrix44.from_x_rotation(0.7 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.7 * glfw.get_time())
    rot_z = pyrr.Matrix44.from_z_rotation(0.5 * glfw.get_time())
    rotation = pyrr.matrix44.multiply(rot_z, rot_y)

    # Draw Sushi 🍣
    model = pyrr.matrix44.multiply(rotation, sushi_pos)
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Plate 🧫
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, plate_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    # Draw Floor 🟫
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, texture[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sushi_indices))

    glfw.swap_buffers(window)

glfw.terminate()
