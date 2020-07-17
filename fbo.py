import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from PIL import Image
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 684

NEAR_PLANE = 1.0
FAR_PLANE = 1000.0

render_texture = None



fbo = None
texture = None
vex, circle_indices, main_indices, shader = None, None, None, None

def setup_resource():
    # 创建纹理
    global render_texture, fbo
    render_texture = glGenTextures(1)
    fbo = glGenFramebuffers(1)

    glBindTexture(GL_TEXTURE_2D, render_texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, SCREEN_WIDTH, SCREEN_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glBindTexture(GL_TEXTURE_2D, 0)

    # FBO
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_texture, 0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    global texture
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
    image = Image.open("res/smog.jpg")
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    print(image.width, image.height)
    # 要求必须是2的幂
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    global vex, circle_indices, main_indices
    #        positions    colors    texture coords
    vex = [-1, -1, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
           1, -1, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
           1, 1, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
           -1, 1, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,

           ]
    outer = [(455, 262, 4),
             (441, 230, 5),
             (422,194, 6),
             (393,171, 7),
             (376,149, 8),
             (371,104, 9),
             (378,64, 10),
             (401,25, 11),
             (448,15, 12),
             (489,34, 13),
             (515,67, 14),
             (544,112, 15),
             (545,154, 16),
             (541,191, 17),
             (522,239, 18),
             (506,264, 19),
    ]
    inner = [(474,249, 20),
             (463,218, 21),
             (458,180, 22),
             (432,158, 23),
             (468,156, 24),
             (412,123, 25),
             (453,124, 26),
             (420,79, 27),
             (447,90, 28),
             (455,53, 29),
             (478,65, 30),
             (498,88, 31),
             (488,117, 32),
             (519,117, 33),
             (503,154, 34),
             (496,193, 35),
             (496,227, 36),
    ]
    # 归一化，* 2 ，移动(-1, 1)
    coord_x = lambda _: _ * 2 / image.width - 1
    coord_y = lambda _: _ * 2 / image.height - 1
    texture_x = lambda _: _ / image.width
    texture_y = lambda _: _ / image.height
    # 0.1表示outer 0.9 表示inner
    for x, y, _ in outer:
        vex += [coord_x(x), -coord_y(y), 0.0, 0.1, 0.0, 0.0, texture_x(x), texture_y(y)]
    for x, y, _ in inner:
        vex += [coord_x(x), -coord_y(y), 0.0, 0.9, 0.0, 0.0, texture_x(x), texture_y(y)]

    vex = numpy.array(vex, dtype=numpy.float32)

    circle_indices = [
        4, 20, 19,
        4, 5, 20,
        5, 20, 21,
        5,6,21,
        6,21,22,
        6,22,23,
        6,7,23,
        7,8,23,
        8,23,25,
        8,9,25,
        9,25,27,
        9,10,27,
        10,11,27,

        22,23,24,
        23,24,26,
        23,25,26,
        25,26,28,
        25,27,28,
        27,28,29,
        11,27,29,
        11,12,29,

        36,20,21,
        21,35,36,
        21,22,35,
        22,24,35,
        24,34,35,
        24,26,34,
        26,32,34,
        26,28,32,
        28,30,32,
        28,29,30,

        12,13,29,
        13,29,30,
        13,14,30,
        14,30,31,
        14,31,33,
        30,31,32,
        31,32,33,
        32,33,34,
        14,15,33,
        15,16,33,
        33,34,16,
        16,17,34,
        34,35,17,
        35,17,18,
        35,36,18,
        18,36,20,
        18,19,20

    ]
    main_indices = [
        0, 1, 2, 0, 2, 3
    ]

    main_indices = numpy.array(main_indices, dtype=numpy.uint32)
    circle_indices = numpy.array(circle_indices, dtype=numpy.uint32)


def fbo_render():
    # 自定义Framebuffer是不展示的，只是用于临时存储
    global texture, render_texture, fbo
    glBindTexture(GL_TEXTURE_2D, texture)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    EBO = glGenBuffers(1)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, main_indices.itemsize * len(main_indices), main_indices, GL_STATIC_DRAW)
    # glDrawElements(GL_TRIANGLES, len(main_indices), GL_UNSIGNED_INT, None)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, circle_indices.itemsize * len(circle_indices), circle_indices, GL_STATIC_DRAW)
    glDrawElements(GL_TRIANGLES, len(circle_indices), GL_UNSIGNED_INT, None)

    # 绑定默认FBO（窗体帧缓冲区的ID是0）
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glBindTexture(GL_TEXTURE_2D, render_texture)
    # #
    xDiff = glGetUniformLocation(shader, "xDiff")
    glUniform1f(xDiff, 1.0)
    # # #
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, circle_indices.itemsize * len(circle_indices), circle_indices, GL_STATIC_DRAW)
    glDrawElements(GL_TRIANGLES, len(circle_indices), GL_UNSIGNED_INT, None)

    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, main_indices.itemsize * len(main_indices), main_indices, GL_STATIC_DRAW)
    # glDrawElements(GL_TRIANGLES, len(main_indices), GL_UNSIGNED_INT, None)

    # texture = render_texture


def main():

    # initialize glfw
    if not glfw.glfwInit():
        return

    window = glfw.glfwCreateWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "My OpenGL window", None, None)

    if not window:
        glfw.glfwTerminate()
        return

    glfw.glfwMakeContextCurrent(window)

    vertex_shader = """
     #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 colors;
    in layout(location = 2) vec2 textureCoords;
    out vec2 newTexture;
    uniform float xDiff;
    vec3 newPosition; 
    vec2 tmpTexture; 
    void main()
    {
        newPosition.xyz = position.xyz;
        tmpTexture.xy = textureCoords.xy;
        
        if (xDiff == 1.0){
            tmpTexture.y = 1.0 - tmpTexture.y;
            newTexture = vec2(tmpTexture);
        }else{
         tmpTexture.y = tmpTexture.y;
            //newTexture = textureCoords;
        }
        newTexture = vec2(tmpTexture);
        gl_Position = vec4(newPosition, 1.0f);

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
    setup_resource()
    global shader
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
    if status != GL_FRAMEBUFFER_COMPLETE:
        print('error {}'.format(status))
    

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
    glEnable(GL_TEXTURE_2D)
    glUseProgram(shader)
    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    while not glfw.glfwWindowShouldClose(window):
        glfw.glfwPollEvents()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # EBO = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, main_indices.itemsize * len(main_indices), main_indices, GL_STATIC_DRAW)
        #
        # glDrawElements(GL_TRIANGLES, len(main_indices), GL_UNSIGNED_INT, None)
        #
        fbo_render()
        glfw.glfwSwapBuffers(window)

    glfw.glfwTerminate()

if __name__ == "__main__":
    main()