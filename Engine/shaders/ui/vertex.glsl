#version 450 core

layout (location=0) in vec3 vertes_pos;
layout (location=2) in vec2 vertex_texture_coordinate;

uniform mat4 projection;
uniform mat4 model;

out vec2 fragment_texture_coordinate;

void main() {
    gl_Position = projection * model * vec4(vertes_pos, 1.0);
    fragment_texture_coordinate = vertex_texture_coordinate;
}
