import pdb
import pyroute2
class RouteManager:

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
    def get_routes_from_rules(self):
        iproute = pyroute2.IPRoute()
        routes = iproute.get_routes()
        pdb.set_trace()
        filtered_routes = [route for route in routes if route['attrs']['RTA_TABLE'] not in self.exclusion_filter]
        print("{}".format(filtered_routes))

routeManager = RouteManager()
routeManager.get_routes_from_rules()
