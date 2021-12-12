import os
import pyrr
import pygame
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


def Object(vao_vbo, buffer):
    glBindVertexArray(VAO[vao_vbo])
    glBindBuffer(GL_ARRAY_BUFFER, VBO[vao_vbo])
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes,
                 buffer, GL_STATIC_DRAW)
    # Define Vertex and Texture Shader
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          buffer.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                          buffer.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                          buffer.itemsize * 8, ctypes.c_void_p(20))


# Load Object to shader
Object(0, sushi_buffer)
Object(1, wallSide_buffer)
Object(2, table_buffer)
Object(3, floor_buffer)
Object(4, pot_buffer)
Object(5, chair_buffer)
Object(6, wallBack_buffer)

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
chair1mf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, -15]))
chair1mb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, 10]))
chair1lf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, -15]))
chair1lb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, 10]))
chair1rb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, 10]))
chair1rf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, -15]))
# Chair 2 Position
chair2rf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([10, 0, -3]))
chair2rb_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 0, 22]))
chair2mf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, -3]))
chair2mb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-10, 0, 22]))
chair2lf_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, -3]))
chair2lb_pos = pyrr.matrix44.create_from_translation(
    pyrr.Vector3([-30, 0, 22]))
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
# Generate Draw Function
# ==========================================


def DrawObject(vao, pos, tex, ind, scl, rot=no_rotate):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rot)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


def Wall(vao, pos, tex=6, ind=wallSide_indices, scl=floor_scl, rot=no_rotate):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rot)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


def Sushi(pos, vao=0, tex=0, scl=sushi_scl, ind=sushi_indices):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


def Table(pos, vao=2, tex=1, scl=table_scl, ind=table_indices):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


def Pot(pos, vao=4, tex=3, scl=pot_scl, ind=pot_indices):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


def Chair(pos, rot=rotate, vao=5, tex=4, scl=chair_scl, ind=chair_indices):
    glBindVertexArray(VAO[vao])
    glBindTexture(GL_TEXTURE_2D, texture[tex])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pos)
    glUniformMatrix4fv(rotate_loc, 1, GL_FALSE, rot)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scl)
    glDrawArrays(GL_TRIANGLES, 0, len(ind))


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
    DrawObject(0, sushilb_pos, 0, sushi_indices, sushi_scl)
    DrawObject(0, sushilf_pos, 0, sushi_indices, sushi_scl)
    DrawObject(0, sushimb_pos, 0, sushi_indices, sushi_scl)
    DrawObject(0, sushimf_pos, 0, sushi_indices, sushi_scl)
    DrawObject(0, sushirb_pos, 0, sushi_indices, sushi_scl)
    DrawObject(0, sushirf_pos, 0, sushi_indices, sushi_scl)

    # Draw Table ✨
    DrawObject(2, tablelb_pos, 1, table_indices, table_scl)
    DrawObject(2, tablelf_pos, 1, table_indices, table_scl)
    DrawObject(2, tablemb_pos, 1, table_indices, table_scl)
    DrawObject(2, tablemf_pos, 1, table_indices, table_scl)
    DrawObject(2, tablerb_pos, 1, table_indices, table_scl)
    DrawObject(2, tablerf_pos, 1, table_indices, table_scl)

    # Draw Pot ✨
    DrawObject(4, potlb_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potlf_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potmlb_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potmlf_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potmrb_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potmrf_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potrb_pos, 3, pot_indices, pot_scl)
    DrawObject(4, potrf_pos, 3, pot_indices, pot_scl)

    # Draw Chair ✨
    DrawObject(5, chair1lb_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1lb_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1lf_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1mb_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1mf_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1rb_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair1rf_pos, 4, chair_indices, chair_scl)
    DrawObject(5, chair2lb_pos, 4, chair_indices, chair_scl, rot=rotate)
    DrawObject(5, chair2lf_pos, 4, chair_indices, chair_scl, rot=rotate)
    DrawObject(5, chair2mb_pos, 4, chair_indices, chair_scl, rot=rotate)
    DrawObject(5, chair2mf_pos, 4, chair_indices, chair_scl, rot=rotate)
    DrawObject(5, chair2rb_pos, 4, chair_indices, chair_scl, rot=rotate)
    DrawObject(5, chair2rf_pos, 4, chair_indices, chair_scl, rot=rotate)

    # Draw Floor 🟫
    DrawObject(3, floor_pos, 2, floor_indices, floor_scl)

    # Draw Roof
    DrawObject(3, roof_pos, 5, floor_indices, floor_scl)

    # Draw Wall
    DrawObject(1, wallSideR_pos, 6, wallSide_indices, floor_scl)
    DrawObject(1, wallSideL_pos, 6, wallSide_indices, floor_scl)
    DrawObject(6, wallBack_pos, 6, wallBack_indices, floor_scl)

    pygame.display.flip()

pygame.quit()
