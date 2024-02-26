from Engine.component import Component
from Engine.materials.solid_image import SolidImage
from Engine.mesh import Mesh

from OpenGL.GL import *
from pyrr import matrix44
import numpy
import math


class Billboard(Component):

    def __init__(self, material):
        super().__init__()

        self.material = material
    
    def initialize(self):
        self.material = self.node.scene.app.graphics_engine.materials[self.material]

        width, height = (1, 1)
        self.vertices = numpy.array(
            (
                0, -width / 2,  height / 2, 0, 1, -1, 0, 0,
                0, -width / 2, -height / 2, 0, 0, -1, 0, 0,
                0,  width / 2, -height / 2, 1, 0, -1, 0, 0,

                0, -width / 2,  height / 2, 0, 1, -1, 0, 0,
                0,  width / 2, -height / 2, 1, 0, -1, 0, 0,
                0,  width / 2,  height / 2, 1, 1, -1, 0, 0
            ),
            dtype=numpy.float32
        )

        self.vertex_count = 6
        stride = Mesh.INT_BITSIZE * Mesh.VERTEX_SIZE

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
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        # Vertex normal
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

        # Vertex texture coord
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(24))
    
    def render(self):
        distance_from_camera = self.node.transform.get_global_position() - self.node.scene.camera.position
        angle_z = numpy.arctan2(-distance_from_camera[1], distance_from_camera[0])
        dist2d = math.sqrt(distance_from_camera[0] ** 2 + distance_from_camera[1] ** 2)
        angle_y = numpy.arctan2(distance_from_camera[2], dist2d)

        billboard_transform = matrix44.create_identity(numpy.float32)
        billboard_transform = matrix44.multiply(
            billboard_transform,
            matrix44.create_from_y_rotation(angle_y, dtype=numpy.float32)
        )
        billboard_transform = matrix44.multiply(
            billboard_transform,
            matrix44.create_from_z_rotation(angle_z, dtype=numpy.float32)
        )
        billboard_transform = matrix44.multiply(
            billboard_transform,
            matrix44.create_from_translation(self.node.transform.get_global_position(), dtype=numpy.float32)
        )

        self.material.use(self.node)
        glUniformMatrix4fv(self.material.model_uniform_location, 1, GL_FALSE, billboard_transform)
        glBindVertexArray(self.vertex_array_object)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vertex_array_object,))
        glDeleteBuffers(1, (self.vertex_buffer_object,))
