import OpenGL.GL.shaders
import numpy
from OpenGL.GL import *
from PIL import Image

import glfw


def main():
    # initialize glfw
    if not glfw.glfwInit():
        return
    window = glfw.glfwCreateWindow(800, 600, "My OpenGL window", None, None)

    if not window:
        glfw.glfwTerminate()
        return

    glfw.glfwMakeContextCurrent(window)
    #           positions        colors          texture coords
    quad = [   -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
               -0.5,  0.5, 0.0,  1.0, 1.0, 1.0,  0.0, 1.0]

    quad = numpy.array(quad, dtype = numpy.float32)

    indices = [0, 1, 2,
               2, 3, 0]

    indices = numpy.array(indices, dtype= numpy.uint32)

    print(quad.itemsize * len(quad))
    print(indices.itemsize * len(indices))
    print(quad.itemsize * 8)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 color;
    in layout(location = 2) vec2 inTexCoords;

    out vec3 newColor;
    out vec2 outTexCoords;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
        outTexCoords = inTexCoords;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;
    in vec2 outTexCoords;

    out vec4 outColor;
    uniform sampler2D samplerTex;
    void main()
    {
        outColor = texture(samplerTex, outTexCoords) * vec4(newColor, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, quad.itemsize * len(quad), quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    #position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    #color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    #texture_coords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)



    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    #texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # image = Image.open("res/smiley.png")
    image = Image.open("res/egg.png")
    #img_data = numpy.array(list(image.getdata()), numpy.uint8)
    img_data = image.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
    # img_data= flipped_image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    #print(image.width, image.height)




    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)

    while not glfw.glfwWindowShouldClose(window):
        glfw.glfwPollEvents()

        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.glfwSwapBuffers(window)

    glfw.glfwTerminate()

if __name__ == "__main__":
    main()