import glfw
from OpenGL.GL import *
import numpy as np
from math import sin, cos


def main():
    # Initialize the library , window, & context
    if not glfw.init():
        raise Exception('glfw can\'t be initialized')

    window = glfw.create_window(640, 480, "Grafkomku", None, None)

    if not window:
        glfw.terminate()
        raise Exception('glfw window can\'t be created')

    glfw.set_window_pos(window, 100, 100)
    glfw.make_context_current(window)
    glClearColor(0, 0, 0.1, 0)

    # Define vertices and color
    vertices = [0, 0.5, 0,
                - 0.5, -0.5, 0,
                0.5, -0.5, 0]
    vertices = np.array(vertices, dtype=float)

    colors = [1, 0, 0,
              0, 1, 0,
              0, 0, 1]
    colors = np.array(colors, dtype=float)

    # Make Shape from Array
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):

        # Swap and clear buffer and Poll process events
        glfw.swap_buffers(window)
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.poll_events()

        # Draw & Tranformation the objext
        glDrawArrays(GL_TRIANGLES, 0, 3)
        # returns the elapsed time, since init was called
        ct = glfw.get_time()
        glLoadIdentity()
        glScale(abs(sin(ct)), abs(sin(ct)), 1)
        glRotatef(sin(ct) * 45, 0, 0, 1)
        glTranslatef(sin(ct), cos(ct), 0)

    glfw.terminate()


if __name__ == "__main__":
    main()
