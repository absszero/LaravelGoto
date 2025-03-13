class RouteItem:

    def __init__(self, route, place):
        if 'GET|HEAD' == route['method']:
            route['method'] = 'GET'

        self.label = route['method'] + ' ' + route['uri']
        self.detail = route['action']
        self.place = place
