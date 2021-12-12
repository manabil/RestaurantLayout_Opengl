import glfw
from OpenGL.GL import *


def main():
    # Initialize the library
    if not glfw.init():
        raise Exception('glfw can\'t be initialized')

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        raise Exception('glfw window can\'t be created')

    # Make the window's context current
    glfw.make_context_current(window)

    # Coloring window
    glClearColor(0, 0, 0.1, 0)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyOpenGL

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Clear Buffer color
        glClear(GL_COLOR_BUFFER_BIT)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
