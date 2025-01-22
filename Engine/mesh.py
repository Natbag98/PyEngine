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
    
    def get_local_xyz_vertices(self, with_sperated_vertices=False, with_seperated_channels=False):
        if not with_seperated_channels:
            xyz_vertices = []
        else:
            xyz_vertices = [[], [], []]

        for i in range(self.vertex_count):
            vertex = self.vertex_size * i
            if with_seperated_channels:
                xyz_vertices[0].append(self.vertices[vertex])
                xyz_vertices[1].append(self.vertices[vertex + 1])
                xyz_vertices[2].append(self.vertices[vertex + 2])
            elif with_sperated_vertices:
                xyz_vertices.append(
                    (
                        self.vertices[vertex],
                        self.vertices[vertex + 1],
                        self.vertices[vertex + 2]
                    )
                )
            else:
                xyz_vertices.append(self.vertices[vertex])
                xyz_vertices.append(self.vertices[vertex + 1])
                xyz_vertices.append(self.vertices[vertex + 2])
        
        return xyz_vertices

    def destroy(self):
        glDeleteVertexArrays(1, (self.vertex_array_object,))
        glDeleteBuffers(1, (self.vertex_buffer_object,))
