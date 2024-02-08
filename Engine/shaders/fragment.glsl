#version 450 core

in vec2 fragment_texture_coord;

uniform vec3 color;

out vec4 fragment_color;

void main() {
    fragment_color = vec4(color, 1.0);
}
