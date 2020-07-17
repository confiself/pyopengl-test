import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy


def main():

    # initialize glfw
    if not glfw.glfwInit():
        return


    window = glfw.glfwCreateWindow(800, 600, "My OpenGL window", None, None)

    if not window:
        glfw.glfwTerminate()
        return

    glfw.glfwMakeContextCurrent(window)
    #           positions        colors
    quad = [   -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
                0.5,  0.5, 0.0,  0.0, 0.0, 1.0,
               -0.5,  0.5, 0.0,  1.0, 1.0, 1.0]

    quad = numpy.array(quad, dtype = numpy.float32)

    indices = [0, 1, 2,
               2, 3, 0]

    indices = numpy.array(indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
         outColor = vec4(newColor, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 96, quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)

    # 用于替换背景色，否则是黑色的背景
    glClearColor(0.2, 0.3, 0.2, 1.0)

    while not glfw.glfwWindowShouldClose(window):
        glfw.glfwPollEvents()

        glClear(GL_COLOR_BUFFER_BIT)
        # 这里的6代表索引的个数，决定画三角形的多少，如果为3则只画一个三角形
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.glfwSwapBuffers(window)
    glfw.glfwTerminate()

if __name__ == "__main__":
    main()
