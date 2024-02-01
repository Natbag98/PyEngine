

class WavefrontLoader:
    
    def __init__(self):
        self.v = []
        self.vn = []
        self.vt = []
        self.vertices = []

    def load(self, filename):
        self.v = []
        self.vn = []
        self.vt = []
        self.vertices = []

        object_count = 0
        with open(filename, 'r') as file:
            for line in file.readlines():
                data = [d.replace('\n', '') for d in line.split(' ')]
                data_type = data.pop(0)

                if data_type == 'o':
                    object_count += 1
                    if object_count > 1:
                        raise Exception(f'Found multiple objects in wavefront file: {filename}')
                
                if data_type == 'v':
                    self.v.append(self.read_vec3_data(data))
                elif data_type == 'vn':
                    self.vn.append(self.read_vec3_data(data))
                elif data_type == 'vt':
                    self.vt.append(self.read_vec2_data(data))
                elif data_type == 'f':
                    self.read_face_data(data)
        
        return self.vertices

    def read_face_data(self, data):
        tri_count = len(data) - 2
        for i in range(tri_count):
            self.make_corner(data[0])
            self.make_corner(data[1 + i])
            self.make_corner(data[2 + i])

    def make_corner(self, corner_data: str):
        corner_v, corner_vt, corner_vn = corner_data.split('/')
        [self.vertices.append(element) for element in self.v[int(corner_v) - 1]]
        [self.vertices.append(element) for element in self.vn[int(corner_vn) - 1]]
        [self.vertices.append(element) for element in self.vt[int(corner_vt) - 1]]
    
    def read_vec3_data(self, data):
        return [
            float(data[0]),
            float(data[1]),
            float(data[2])
        ]

    def read_vec2_data(self, data):
        return [
            float(data[0]),
            float(data[1])
        ]
