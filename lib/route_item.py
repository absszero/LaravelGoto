class RouteItem:


    def __init__(self, route, place):
        self.label = route['uri']
        self.description = route['method']
        self.detail = route['action']
        self.place = place
