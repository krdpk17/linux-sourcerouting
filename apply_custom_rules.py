import pdb
import pyroute2
class RouteManager:

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = {}
        self.ip_routes = {}
        self.routes_by_priority = {}
    
    def parse_rule(self, rule):
        rule_attrs = rule['attrs']
        pdb.set_trace()
        attr_dict = {attr[0]:attr[1] for attr in attrs}

    def fetch_rules(self):
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        rules = iproute.get_rules()
        self.ip_rules = [lambda rule: self.parse_rule(rule) for rule in rules if rule['table'] not in self.exclusion_filter]
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
