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
    #        positions    colors    texture coords
    vex = [-0.5, -0.5,  0.0, 1.0, 0.0, 0.0,   0.0, 0.0,
            0.5, -0.5,  0.0, 1.0, 0.0, 0.0,  1.0, 0.0,
            0.5,  0.5,  0.0, 1.0, 0.0, 0.0,  1.0, 1.0,
            -0.5,  0.5,  0.0, 1.0, 0.0, 0.0,   0.0, 1.0,

           0.03, 0.04, 0.0, 0.9, 0.0, 0.0,  0.53, 0.54,
           -0.14,0.03, 0.0,1.0, 0.0, 0.0,  0.36, 0.53,
           0.01, 0.23, 0.0,1.0, 0.0, 0.0, 0.51, 0.73,
           0.2, 0.05, 0.0,1.0, 0.0, 0.0,  0.7, 0.55,
           0.02, -0.12, 0.0,1.0, 0.0, 0.0, 0.52, 0.38,
          ]

    vex = numpy.array(vex, dtype = numpy.float32)

    circle_indices = [
        4, 5, 6,7, 8, 5
    ]
    main_indices = [
                0, 1, 2, 0, 2, 3
               ]

    main_indices = numpy.array(main_indices, dtype= numpy.uint32)
    circle_indices = numpy.array(circle_indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 colors;
    in layout(location = 2) vec2 textureCoords;
    out vec2 newTexture;
    uniform float xDiff;
    vec3 newPosition; 
    void main()
    {
        newPosition.xyz = position.xyz;
        if ( colors.r == 0.9){
            newPosition.x = newPosition.x + xDiff;
            newPosition.y = newPosition.y + xDiff;
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
    glBufferData(GL_ARRAY_BUFFER, vex.itemsize * len(vex), vex, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vex.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #color
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vex.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    #texture
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vex.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)


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
    image = Image.open("res/egg.jpg")
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

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, main_indices.itemsize * len(main_indices), main_indices, GL_STATIC_DRAW)


        # glDrawElements(GL_TRIANGLES, len(main_indices), GL_UNSIGNED_INT, None)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, circle_indices.itemsize * len(circle_indices), circle_indices, GL_STATIC_DRAW)
        value = ((int(math.modf(glfw.glfwGetTime())[0] * 100)) % 30 - 15) / 30 / 10
        print(value)
        xDiff = glGetUniformLocation(shader, "xDiff")
        glUniform1f(xDiff, value * 0.5)
        glDrawElements(GL_TRIANGLE_FAN, len(circle_indices), GL_UNSIGNED_INT, None)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, main_indices.itemsize * len(main_indices), main_indices, GL_STATIC_DRAW)


        glDrawElements(GL_TRIANGLES, len(main_indices), GL_UNSIGNED_INT, None)

        glfw.glfwSwapBuffers(window)

    glfw.glfwTerminate()

if __name__ == "__main__":
    main()