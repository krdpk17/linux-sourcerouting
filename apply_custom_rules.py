import pdb
import pyroute2
class RouteManager:

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = {}
    def get_rules_priority(self):
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        rules = iproute.get_rules()
        self.ip_rules = [rule for rule in rules if rule['lookup'] not in self.exclusion_filter]
        return
    def get_routes(self):
        iproute = pyroute2.IPRoute()
        routes = iproute.get_routes()
        pdb.set_trace()
        filtered_routes = [route for route in routes if route['table'] not in self.exclusion_filter]
        print("{}".format(filtered_routes))

    def process_custom_rules(self):
        ip_rules = self.get_rules_priority()
        ip_routes = self.get_routes()
routeManager = RouteManager()
routeManager.process_custom_rules()
