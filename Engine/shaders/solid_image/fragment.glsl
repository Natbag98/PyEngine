#version 450 core

in vec2 fragment_texture_coordinate;

out vec4 color;

uniform sampler2D imageTexture;

void main() {
    color = texture(imageTexture, fragment_texture_coordinate);
}
