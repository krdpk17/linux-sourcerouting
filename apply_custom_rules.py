import pdb
import pyroute2

'''
    TODO: 
    Check purpose of multiple rules with same table ID
    Check whether ordering of route entries for a table matters. Try to maintain same order
'''
class RouteManager:

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = {}
        self.ip_routes = []
        self.routes_by_priority = {}
    
    def parse_rule(self, rule):
        rule_attrs = rule['attrs']
        attr_dict = {attr[0]:attr[1] for attr in rule_attrs}
        return attr_dict

    def parse_route(self, route):
        table_id = route['table']
        if table_id not in self.ip_rules:
            print("Couldn't find ip rule priority for {} table id and {} route".format(table_id, route))
            return
        priority = self.ip_rules[table_id]['FRA_PRIORITY']
        return (priority, route)

    def fetch_rules(self):
        iproute = pyroute2.IPRoute()
        rules = iproute.get_rules()
        self.ip_rules = {rule['table']:(lambda rule: self.parse_rule(rule))(rule) for rule in rules if rule['table'] not in self.exclusion_filter}
        print("Found {} rules".format(len(self.ip_rules)))
        return
    
    def merge_routes_by_priority(self):
        routes = self.ip_routes
        routes_by_priority = self.routes_by_priority
        pdb.set_trace()
        for route in routes:
            priority = route[0]
            if priority not in self.routes_by_priority:
                routes_by_priority[priority] = []
            routes_by_priority[priority].append(route[1])
        print("Number of entries after priority based merge is {}".format(len(routes_by_priority)))
        return


    def fetch_routes(self):
        iproute = pyroute2.IPRoute()
        routes = iproute.get_routes()
        self.ip_routes = [(lambda route: self.parse_route(route))(route)  for route in routes if route['table'] not in self.exclusion_filter]
        print("Found {} routes".format(len(self.ip_routes)))
        self.merge_routes_by_priority()
        return
    
    def routes_to_command(self):
        pdb.set_trace()

    def process_custom_rules(self):
        self.fetch_rules()
        self.fetch_routes()
        self.routes_to_command()
routeManager = RouteManager()
routeManager.process_custom_rules()
