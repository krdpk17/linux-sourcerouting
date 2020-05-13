import pdb
import pyroute2

class Tests:
    def __init__(self):
        self.table_id_single_rule = 100
        self.table_id_multiple_rule = 200
        self.gateway = '172.17.0.3'
    
    def write_to_file(self, file_name, commands):
        with open(file_name, 'w') as the_file:
            for command in commands:
                the_file.write(command + '\n')
    
    def test_sorting(self):
        '''
            This testcase allows verifies that order of routes are following most specific to least specific
        '''
        iproute = pyroute2.IPRoute()
        #Add rule
        iproute.rule('add', self.table_id_single_rule, 32000, src='1.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        iproute.route("add", dst="10.100.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        iproute.route("add", dst="10.100.10.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        expected_output = [
            'add ns pbr  pbr_32000_101  -destIP 10.100.10.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 101 ALLOW',
            'add ns pbr  pbr_32000_102  -destIP 10.100.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 102 ALLOW',
            'add ns pbr  pbr_32000_103  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 103 ALLOW',
            'add ns pbr  pbr_32000_104  -destIP 0.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 104 ALLOW',
        ]
        self.write_to_file('test_sorting.txt', expected_output)       
    
    def create_single_rule_multiple_route(self):
        iproute = pyroute2.IPRoute()
        #Add rule
        iproute.rule('add', self.table_id_single_rule, 32000, src='1.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        iproute.route("add", dst="11.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        expected_output = [
            'add ns pbr  pbr_32000_101  -destIP 0.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 101 ALLOW',
            'add ns pbr  pbr_32000_102  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 102 ALLOW',
            'add ns pbr  pbr_32000_103  -destIP 11.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 103 ALLOW'
        ]
        self.write_to_file('create_single_rule_multiple_route.txt', expected_output)
    def create_multiple_rule_single_route(self):
        iproute = pyroute2.IPRoute()
        #Add rule
        iproute.rule('add', self.table_id_single_rule, 32000, src='1.1.1.1')
        iproute.rule('add', self.table_id_single_rule, 32001, src='2.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_single_rule)
        expected_output = [
            'add ns pbr  pbr_32000_101  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 101 ALLOW',
            'add ns pbr  pbr_32001_102  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 2.1.1.1 -priority 102 ALLOW',
        ]
        self.write_to_file('create_multiple_rule_single_route.txt', expected_output)
    def create_multi_rule_multiple_route(self):
        iproute = pyroute2.IPRoute()
        #Add rules with same table ID
        iproute.rule('add', self.table_id_multiple_rule, 32000, src='0.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32001, src='1.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32002, dst='2.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32003, src='3.1.1.1', dst='4.1.1.1')
        #iproute.rule('add', self.table_id_multiple_rule, 32004, srcport='8080')
        #iproute.rule('add', self.table_id_multiple_rule, 32005, dstport='9090')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_multiple_rule)
        iproute.route("add", dst="11.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_multiple_rule)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway=self.gateway, table=self.table_id_multiple_rule)

        expected_output = [
            'add ns pbr  pbr_32000_101  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 0.1.1.1 -priority 101 ALLOW',
            'add ns pbr  pbr_32000_102  -destIP 11.0.0.0 -nextHop 172.17.0.3 -srcIP 0.1.1.1 -priority 102 ALLOW',
            'add ns pbr  pbr_32000_103  -destIP 0.0.0.0 -nextHop 172.17.0.3 -srcIP 0.1.1.1 -priority 103 ALLOW',
            'add ns pbr  pbr_32001_104  -destIP 10.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 104 ALLOW',
            'add ns pbr  pbr_32001_105  -destIP 11.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 105 ALLOW',
            'add ns pbr  pbr_32001_106  -destIP 0.0.0.0 -nextHop 172.17.0.3 -srcIP 1.1.1.1 -priority 106 ALLOW',
        ]
        self.write_to_file('create_multi_rule_multiple_route.txt', expected_output)

    def delete_rules():
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        iproute.rule('delete', self.table_id)

    def cleanup(self):
        self.delete_rules()

    def execute(self):
        # self.test_sorting()
        # self.create_single_rule_multiple_route()
        # self.create_multiple_rule_single_route()
        # self.create_multi_rule_multiple_route()

tests = Tests()
tests.execute()
tests.cleanup()