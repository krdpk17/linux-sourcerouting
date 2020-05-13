import pdb
import pyroute2
from collections import OrderedDict 

'''
    TODO: 
    
    Routes in a table is envaluated from most specific to least specific. So, chronological order doesn't matter. There is no need to maintain order of entry
    Priority odering must be maintained
    Testcase:
    Check with IPV6 configuration
    Handle multiple rules with same table ID
    Check with empty rules
    Check with empty routes
    Check with routes without IP rule
    Check with rule without any route
    check with rule for all traffic [from all lookup 101]
    Check for precedence between rule and routes (rule has higher precedence)
        conficting config between rule and routes (rule has distination and route also has)

'''
class RouteManager:

    class CommandMaping:
        '''
        Maps the attribute names from the IP route
        port mapping is not support by IP and so skipped. 
        'ip rule add sport 8080 dport 9090 table 102' -> 'from all lookup 102'
        '''
        attrs_mapping = {'RTA_GATEWAY':'-nextHop', 'RTA_DST':'-destIP', 'FRA_DST':'-destIP', 'FRA_SRC':'-srcIP'}
        command_prefix = 'add ns pbr '
        command_suffix = 'ALLOW'
        command_name_format = 'pbr_{orig_prio}_{new_prio}'


    def __init__(self, exclusion_filter=[0, 253, 254, 255]):
        self.exclusion_filter = exclusion_filter
        self.ip_rules = []
        self.ip_rules_by_id = {}
        self.ip_rules_by_priority = {}
        self.ip_routes = []
        self.routes_by_priority = {}
        self.base_priority = 100
        self.ip_rules_by_priority = {}
        self.commands = []
    
    def parse_rule(self, rule):
        rule_attrs = rule['attrs']
        attr_dict = {attr[0]:attr[1] for attr in rule_attrs}
        self.ip_rules_by_priority[attr_dict['FRA_PRIORITY']] = attr_dict
        return attr_dict

    def parse_route(self, route):
        table_id = route['table']
        if table_id not in self.ip_rules_by_id or not len(self.ip_rules_by_id[table_id]):
            print("Couldn't find ip rule priority for {} table id and {} route".format(table_id, route['attrs']))
            return None
        rule_list = self.ip_rules_by_id[table_id]
        priority = []
        for rule in rule_list:
            priority.append(rule['FRA_PRIORITY'])
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
            priority_list = route[0]
            for priority in priority_list:
                if priority not in self.routes_by_priority:
                    routes_by_priority[priority] = []
                routes_by_priority[priority].append(route[1])
        self.routes_by_priority = OrderedDict(sorted(routes_by_priority.items()))
        print("Number of entries after priority based merge is {}".format(len(routes_by_priority)))
        return


    def fetch_routes(self):
        iproute = pyroute2.IPRoute()
        routes = iproute.get_routes()
        '''
        Since routes are of list type and so, list comprehension maintains the same order in the result.
        Refer: https://stackoverflow.com/questions/1286167/is-the-order-of-results-coming-from-a-list-comprehension-guaranteed
        '''
        self.ip_routes = [(lambda route: self.parse_route(route))(route)  for route in routes if route['table'] not in self.exclusion_filter]
        print("Removing routes which has no corresponding rules")
        self.ip_routes = [route for route in self.ip_routes if route is not None]
        print("Found {} routes".format(len(self.ip_routes)))
        self.merge_routes_by_priority()
        return
    
    def map_route_to_command(self, route, orig_priority, new_priority):
        command = RouteManager.CommandMaping.command_prefix
        options = {}
        attrs_mapping = RouteManager.CommandMaping.attrs_mapping
        name_format = RouteManager.CommandMaping.command_name_format
        for key, value in route.items():
            if key in attrs_mapping:
                options[attrs_mapping[key]] = value
        pdb.set_trace()
        rule_mapping = self.ip_rules_by_priority[orig_priority]
        for key, value in rule_mapping.items():
            if key in attrs_mapping.items():
                options[attrs_mapping[key]] = value
        options['-priority'] = new_priority
        options_str = ''
        for key, value in options.items():
            option_str = key + ' ' + str(value)
            options_str = options_str + ' ' + option_str
        
        name = name_format.format(orig_prio=orig_priority, new_prio=new_priority)
        command = command + ' ' + name + ' ' + options_str + RouteManager.CommandMaping.command_suffix
        self.commands.append(command)



    def routes_to_command(self):
        routes_by_priority = self.routes_by_priority
        curr_priority = self.base_priority
        for priority, route_list  in routes_by_priority.items():
            for route in route_list:
                curr_priority = curr_priority + 1
                self.map_route_to_command(route, priority, curr_priority)   
        pdb.set_trace()

    def process_custom_rules(self):
        self.fetch_rules()
        self.fetch_routes()
        self.routes_to_command()
routeManager = RouteManager()
routeManager.process_custom_rules()
