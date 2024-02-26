from Engine.Utilities.wavefront_loader import WavefrontLoader

from OpenGL.GL import *
import numpy


class Mesh:
    INT_BITSIZE = 4
    VERTEX_SIZE = 8

    def __init__(self, filename):
        self.stride = self.INT_BITSIZE * self.VERTEX_SIZE

        # v, vn, vt
        self.vertices = numpy.array(WavefrontLoader().load(filename), numpy.float32)
        self.vertex_count = len(self.vertices) // self.VERTEX_SIZE

        # Setup vertex array object
        self.vertex_array_object = glGenVertexArrays(1)
        glBindVertexArray(self.vertex_array_object)

        # Setup vertex buffer object
        self.vertex_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Setup attrib pointers
        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.stride, ctypes.c_void_p(0))

        # Vertex normal
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.stride, ctypes.c_void_p(12))

        # Vertex texture coord
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.stride, ctypes.c_void_p(24))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vertex_array_object,))
        glDeleteBuffers(1, (self.vertex_buffer_object,))
