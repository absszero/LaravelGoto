class Place:

    def __init__(self, path, location=None, uri=None):
        self.path = path
        self.location = location
        self.is_controller = False
        self.paths = []
        self.uri = uri
