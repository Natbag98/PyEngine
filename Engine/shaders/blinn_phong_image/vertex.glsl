#version 450 core

layout (location=0) in vec3 vertes_pos;
layout (location=1) in vec3 vertex_normal;
layout (location=2) in vec2 vertex_texture_coordinate;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fragment_texture_coordinate;
out vec3 fragment_position;
out vec3 fragment_normal;

void main() {
    gl_Position = projection * view * model * vec4(vertes_pos, 1.0);

    fragment_texture_coordinate = vertex_texture_coordinate;
    fragment_position = (model * vec4(vertes_pos, 1.0)).xyz;
    fragment_normal = mat3(model) * vertex_normal;
}
