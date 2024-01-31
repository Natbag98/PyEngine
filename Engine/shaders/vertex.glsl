#version 450 core

layout (location=0) in vec3 vertes_pos;
layout (location=1) in vec3 vertex_normal;
layout (location=2) in vec2 vertex_texture_coord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fragment_texture_coord;

void main() {
    gl_Position = projection * view * model * vec4(vertes_pos, 1.0);
    fragment_texture_coord = vertex_texture_coord;
}
