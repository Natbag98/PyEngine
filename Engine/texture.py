from OpenGL.GL import *
import pygame


class Texture:

    def __init__(self, filename):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # Setup texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Load image, generate mipmaps
        image = pygame.image.load(filename).convert_alpha()
        image_size = image.get_size()
        image_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_size[0], image_size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))
