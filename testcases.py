import pdb
import pyroute2

class Tests:
    def __init__(self):
        self.table_id_single_rule = 100
        self.table_id_multiple_rule = 200
    def create_single_rule_multiple_routes(self):
        iproute = pyroute2.IPRoute()
        #Add rule
        iproute.rule('add', self.table_id_single_rule, 32000, src='1.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_single_rule)
        iproute.route("add", dst="11.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_single_rule)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_single_rule)
    def create_multi_rule_multiple_routes(self):
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        #Add rules with same table ID
        iproute.rule('add', self.table_id_multiple_rule, 32000, src='1.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32001, src='2.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32002, dst='2.1.1.1')
        iproute.rule('add', self.table_id_multiple_rule, 32002, src='3.1.1.1', dst='4.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_multiple_rule)
        iproute.route("add", dst="11.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_multiple_rule)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id_multiple_rule)
    def delete_rules():
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        iproute.rule('delete', self.table_id)

    def cleanup(self):
        self.delete_rules()

    def execute(self):
        self.create_single_rule_multiple_routes()
        self.create_multi_rule_multiple_routes()

tests = Tests()
tests.execute()
tests.cleanup()