#version 450 core

struct PointLight {
    vec3 position;
    vec3 color;
    float strength;
};

in vec2 fragment_texture_coordinate;
in vec3 fragment_position;
in vec3 fragment_normal;

out vec4 color;

uniform sampler2D imageTexture;
uniform PointLight point_lights[100];
uniform float ambient_light;
uniform float specular_strength;
uniform vec3 camera_position;

vec3 calculate_point_light(PointLight _point_light, vec3 _fragment_position, vec3 _fragment_normal, vec3 _base_texture);

void main() {
    vec3 temp_color = vec3(0.0);
    vec3 base_texture = texture(imageTexture, fragment_texture_coordinate).rgb;

    // Ambient lighting
    temp_color += ambient_light * base_texture;

    for (int i = 0; i < 100; i++) {
        temp_color += calculate_point_light(point_lights[i], fragment_position, fragment_normal, base_texture);
    }

    color = vec4(temp_color, 1.0);
}

vec3 calculate_point_light(PointLight _point_light, vec3 _fragment_position, vec3 _fragment_normal, vec3 _base_texture) {
    vec3 result = vec3(0.0);

    // Calculate geometric data
    vec3 frag_to_light = _point_light.position - _fragment_position;
    float frag_to_light_distance = length(frag_to_light);
    frag_to_light = normalize(frag_to_light);
    vec3 frag_to_camera = normalize(_fragment_position - camera_position);
    vec3 half_vec = normalize(frag_to_light - frag_to_camera);

    // Diffuse lighting
    result += _point_light.color * _point_light.strength * max(0.0, dot(_fragment_normal, frag_to_light)) / pow(frag_to_light_distance, 2.0) * _base_texture;

    // Specular lighting
    result += _point_light.color * _point_light.strength * pow(max(0.0, dot(_fragment_normal, half_vec)), specular_strength) / pow(frag_to_light_distance, 2.0);

    return result;
}
