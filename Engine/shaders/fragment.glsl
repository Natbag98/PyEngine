#version 450 core

in vec2 fragment_texture_coord;

uniform vec3 object_color;

out vec4 color;

void main() {
    color = vec4(object_color, 1.0);
}
