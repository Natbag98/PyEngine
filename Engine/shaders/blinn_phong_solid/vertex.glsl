#version 450 core

layout (location=0) in vec3 vertes_pos;
layout (location=1) in vec3 vertex_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 fragment_position;
out vec3 fragment_normal;

void main() {
    gl_Position = projection * view * model * vec4(vertes_pos, 1.0);

    fragment_position = (model * vec4(vertes_pos, 1.0)).xyz;
    fragment_normal = mat3(model) * vertex_normal;
}
