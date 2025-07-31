

class WavefrontLoader:
    
    def __init__(self):
        self.v = []
        self.vn = []
        self.vt = []
        self.vertices: dict[str, list] = {}
        self.filename = None

    def load(self, filename, to_return: str='first'):
        self.v = []
        self.vn = []
        self.vt = []
        self.vertices: dict[str, list]  = {}
        self.filename = filename

        with open(filename, 'r') as file:
            current_object = ''
            for line in file.readlines():
                data = [d.replace('\n', '') for d in line.split(' ')]
                data_type = data.pop(0)

                if data_type == 'o':
                    self.vertices[data[0]] = []

                if data_type == 'o':
                    current_object = data[0]
                elif data_type == 'v':
                    self.v.append(self.read_vec3_data(data))
                elif data_type == 'vn':
                    self.vn.append(self.read_vec3_data(data))
                elif data_type == 'vt':
                    self.vt.append(self.read_vec2_data(data))
                elif data_type == 'f':
                    self.read_face_data(data, current_object)
        
        return self.get(to_return)

    def get(self, get: str='first'):
        if get == 'first':
            return list(self.vertices.values())[0]
        elif get == 'all':
            return self.vertices
        else:
            if get not in self.vertices:
                raise Exception(f'Wavefront file {self.filename} does not contain an object {get}')
            return self.vertices[get]

    def read_face_data(self, data, current_object: str):
        tri_count = len(data) - 2
        for i in range(tri_count):
            self.make_corner(data[0], current_object)
            self.make_corner(data[1 + i], current_object)
            self.make_corner(data[2 + i], current_object)

    def make_corner(self, corner_data: str, current_object: str):
        corner_v, corner_vt, corner_vn = corner_data.split('/')
        [self.vertices[current_object].append(element) for element in self.v[int(corner_v) - 1]]
        [self.vertices[current_object].append(element) for element in self.vn[int(corner_vn) - 1]]
        [self.vertices[current_object].append(element) for element in self.vt[int(corner_vt) - 1]]
    
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
