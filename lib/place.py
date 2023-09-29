class Place:

    def __init__(self, path, location=None):
        self.path = path
        self.location = location
        self.is_controller = False
        self.paths = []
