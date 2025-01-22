import pygame
from component import Component
import pyrr


class Collider(Component):

    def __init__(self, mesh_name, tags_to_collide_with):
        super().__init__()
        self.tags_to_collide_with = tags_to_collide_with

        local_vert = self.node.scene.app.graphics_engine.meshes[mesh_name].get_local_xyz_vertices(with_seperated_channels=True)
        local_min = pygame.Vector3((min(local_vert[0]), min(local_vert[1]), min(local_vert[2])))
        local_max = pygame.Vector3((max(local_vert[0]), max(local_vert[1]), max(local_vert[2])))
        self.local_vert = [
            [local_min.x, local_min.y, local_min.z],
            [local_min.x, local_min.y, local_max.z],
            [local_min.x, local_max.y, local_min.z],
            [local_min.x, local_max.y, local_max.z],
            [local_max.x, local_min.y, local_min.z],
            [local_max.x, local_min.y, local_max.z],
            [local_max.x, local_max.y, local_min.z],
            [local_max.x, local_max.y, local_max.z]
        ]

        self.global_min = None
        self.global_max = None
        self.update()
    
    @staticmethod
    def check_collision_between_colliders(a, b):
        return  a.global_min.x <= b.global_max.x and \
                a.global_max.x >= b.global_min.x and \
                a.global_min.y <= b.global_max.y and \
                a.global_max.y >= b.global_min.y and \
                a.global_min.z <= b.global_max.z and \
                a.global_max.z >= b.global_min.z

    def physics_update(self):
        global_vert = [[], [], []]
        for vert in self.local_vert:
            vert = pyrr.matrix44.apply_to_vector(self.node.transform.get_world_space_matrix(), vert)
            global_vert[0].append(vert[0])
            global_vert[1].append(vert[1])
            global_vert[2].append(vert[2])
        
        self.global_min = pygame.Vector3((min(global_vert[0]), min(global_vert[1]), min(global_vert[2])))
        self.global_max = pygame.Vector3((max(global_vert[0]), max(global_vert[1]), max(global_vert[2])))

        for tag in self.tags_to_collide_with:
            for node in self.node.scene.get_all_nodes_with_tag(tag):
                if node.has_component(Collider):
                    if self.check_collision_between_colliders(self, node.get_component(Collider)):
                        [c.on_collider_hit(node) for c in self.node.components.values()]
