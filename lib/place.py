import json


class Place:
    def __init__(self, path, location=None, uri=None):
        self.path = path
        self.location = location
        self.is_controller = False
        self.uri = uri
        self.paths = []
        self.uris = []
        self.locations = {}
        self.source = None

    def __str__(self):
        return json.dumps({
            "source": self.source,
            "path": self.path,
            "location": self.location,
            "is_controller": self.is_controller,
            "uri": self.uri,
            "paths": self.paths,
            "uris": self.uris,
            "locations": self.locations
        }, sort_keys=True, indent=2)
