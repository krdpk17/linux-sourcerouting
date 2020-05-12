import pdb
import pyroute2

class Tests:
    def __init__(self):
        self.table_id = 100
    def create_rule_add_routes(self):
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        #Add rule
        iproute.rule('add', self.table_id, 32000, src='1.1.1.1')
        #Add routes
        iproute.route("add", dst="10.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id)
        iproute.route("add", dst="11.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id)
        iproute.route("add", dst="0.0.0.0", mask=24, gateway="172.17.0.3", table=self.table_id)
    def delete_rules():
        iproute = pyroute2.IPRoute()
        pdb.set_trace()
        iproute.rule('delete', self.table_id)

    def cleanup(self):
        self.delete_rules()

    def execute(self):
        self.create_rule_add_routes()

tests = Tests()
tests.execute()
tests.cleanup()