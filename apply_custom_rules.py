import pdb
import pyroute2
class RouteManager:

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = {}
        self.ip_routes = {}

    def fetch_rules(self):
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        rules = iproute.get_rules()
        self.ip_rules = [rule for rule in rules if rule['table'] not in self.exclusion_filter]
        print("Found {} rules".format(len(self.ip_rules)))
        return

    def fetch_routes(self):
        iproute = pyroute2.IPRoute()
        routes = iproute.get_routes()
        pdb.set_trace()
        self.ip_routes = [route for route in routes if route['table'] not in self.exclusion_filter]
        print("Found {} routes".format(len(self.ip_routes)))
        return

    def process_custom_rules(self):
        self.fetch_rules()
        self.fetch_routes()
routeManager = RouteManager()
routeManager.process_custom_rules()
