import pdb
import pyroute2

'''
    TODO: 
    Handle multiple rules with same table ID
    Check whether ordering of route entries for a table matters. Try to maintain same
    Check with IPV6 configuration
    Check with empty rules
    Check with empty routes
    Check with routes without IP rule
    Check with rule without any route
    check with rule for all traffic [from all lookup 101]
    Check for precedence between rule and routes (rule has higher precedence)
        conficting config between rule and routes (rule has distination and route also has)

'''
class RouteManager:

    class OptionsMaping:
        '''
        Maps the attribute names from the IP route
        port mapping is not support by IP and so skipped. 
        'ip rule add sport 8080 dport 9090 table 102' -> 'from all lookup 102'
        '''
        attrs_mapping = {'RTA_GATEWAY':'nextHop', 'RTA_DST':'-destIP', 'FRA_DST':'-destIP', 'FRA_SRC':'srcIP'}

    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = []
        self.ip_rules_by_id = {}
        self.ip_routes = []
        self.routes_by_priority = {}
        self.base_priority = 100
    
    def parse_rule(self, rule):
        rule_attrs = rule['attrs']
        attr_dict = {attr[0]:attr[1] for attr in rule_attrs}
        return attr_dict

    def parse_route(self, route):
        table_id = route['table']
        if table_id not in self.ip_rules_by_id or not len(self.ip_rules_by_id[table_id]):
            print("Couldn't find ip rule priority for {} table id and {} route".format(table_id, route['attrs']))
            return None
        priority = self.ip_rules_by_id[table_id][0]['FRA_PRIORITY']
        attrs = {attr[0]:attr[1] for attr in route['attrs']}
        return (priority, attrs)

    def fetch_rules(self):
        iproute = pyroute2.IPRoute()
        rules = iproute.get_rules()
        self.ip_rules = [(rule['table'], (lambda rule: self.parse_rule(rule))(rule)) for rule in rules if rule['table'] not in self.exclusion_filter]
        print("Found {} rules".format(len(self.ip_rules)))
        self.merge_rules_by_id()
        return

    def merge_rules_by_id(self):
        rules = self.ip_rules
        ip_rules_by_id = self.ip_rules_by_id
        for rule in rules:
            id = rule[0]
            if id not in self.ip_rules_by_id:
                ip_rules_by_id[id] = []
            ip_rules_by_id[id].append(rule[1])
        print("Number of entries after id based merge is {}".format(len(ip_rules_by_id)))
        return

    def merge_routes_by_priority(self):
        routes = self.ip_routes
        routes_by_priority = self.routes_by_priority
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
        print("Removing routes which has no corresponding rules")
        self.ip_routes = [route for route in self.ip_routes if route is not None]
        print("Found {} routes".format(len(self.ip_routes)))
        self.merge_routes_by_priority()
        return
    
    def routes_to_command(self):
        routes_by_priority = self.routes_by_priority
        curr_priority = self.base_priority
        for priority, route_list  in routes_by_priority.items():
             pdb.set_trace()

    def process_custom_rules(self):
        self.fetch_rules()
        self.fetch_routes()
        self.routes_to_command()
routeManager = RouteManager()
routeManager.process_custom_rules()
