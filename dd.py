import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import math
from PIL import Image


def main():

    # initialize glfw
    if not glfw.glfwInit():
        return

    window = glfw.glfwCreateWindow(800, 600, "My OpenGL window", None, None)

    if not window:
        glfw.glfwTerminate()
        return

    glfw.glfwMakeContextCurrent(window)
    #        positions        texture coords
    cube = [-0.5, -0.5,  0.0, 1.0, 0.0, 0.0,   0.0, 0.0,
            0.5, -0.5,  0.0, 1.0, 0.0, 0.0,  1.0, 0.0,
            0.5,  0.5,  0.0, 1.0, 0.0, 0.0,  1.0, 1.0,
            -0.5,  0.5,  0.0, 1.0, 0.0, 0.0,   0.0, 1.0,

           -0.16, -0.18, 0.0,1.0, 0.0, 0.0,  0.34, 0.32,
           0.18, -0.19, 0.0,1.0, 0.0, 0.0, 0.68, 0.31,
           0.16, 0.09, 0.0,1.0, 0.0, 0.0,  0.66, 0.59,
           -0.14, 0.11, 0.0,1.0, 0.0, 0.0, 0.36, 0.61,
          ]

    cube = numpy.array(cube, dtype = numpy.float32)

    indices = [
                0,  4,  7,  0,  1,  4,
               4,  5,  1,  2,  5,  1,
               2,  6,  5,  2,  6,  7,
               2,  3,  7,  3,  7,  0,
               4,  5,  6,  4,  6,  7
               ]

    indices = numpy.array(indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec2 textureCoords;
    out vec2 newTexture;
    uniform float xDiff;
    vec3 newPosition; 
    void main()
    {
        newPosition.xyz = position.xyz; 
        if (position.x >= -0.25 && position.x <= 0.25){
            newPosition.x = newPosition.x + xDiff;
        }
        
        gl_Position = vec4(newPosition, 1.0f);
        newTexture = textureCoords;
    }
    """

    fragment_shader = """
    #version 330
    in vec2 newTexture;

    out vec4 outColor;
    uniform sampler2D samplerTexture;
    void main()
    {
        outColor = texture(samplerTexture, newTexture);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #texture
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(1)


    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    # image = Image.open("res/crate.jpg")
    image = Image.open("res/2egg.jpeg")
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)


    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while not glfw.glfwWindowShouldClose(window):
        glfw.glfwPollEvents()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        value = ((int(math.modf(glfw.glfwGetTime())[0] * 100)) % 30 - 15)  / 30 / 10
        print(value)
        xDiff = glGetUniformLocation(shader, "xDiff")
        glUniform1f(xDiff, value)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)


        glfw.glfwSwapBuffers(window)

    glfw.glfwTerminate()

if __name__ == "__main__":
    main()