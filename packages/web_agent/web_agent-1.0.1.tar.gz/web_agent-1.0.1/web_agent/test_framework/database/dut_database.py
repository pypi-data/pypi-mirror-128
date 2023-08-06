# pylint: disable=broad-except, invalid-name
import os
from utils import log
from test_framework.database.database import SqlConnection
from utils.system import get_ip_address


class DutDatabase(SqlConnection):

    def __init__(self):
        super(DutDatabase, self).__init__(db_name="dutdb")
        self.ip_address = get_ip_address()
        self.port = os.environ.get('agent_port', '5000')
        self.agent_table = "agent"
        self.slot_table = "slot"

    def update_agent(self, agent):
        if self.is_exist_agent(self.ip_address, self.port):
            self.update_exist_agent(agent)
        else:
            self.create_new_agent(agent)

    def update_slot(self, slot_id, slot):
        if slot_id != -1:
            self.update_exist_slot(slot_id, slot)
        else:
            self.create_new_slot(slot)

    def update_exist_slot(self, slot_id, slot):
        update_str = self._covert_dict_2_update_string(**slot)
        update_command = "UPDATE {} SET {} where `id`='{}'".format(self.slot_table, update_str, slot_id)
        self.cursor.execute(update_command)
        self.conn.commit()

    def create_new_slot(self, slot):
        col_str, value_str = self._covert_dict_2_insert_string(**slot)
        insert_command = "INSERT INTO `{}` ({}) VALUES({})".format(self.slot_table, col_str, value_str)
        self.cursor.execute(insert_command)
        self.conn.commit()

    def is_exist_agent(self, ip, port):
        sql_command = "SELECT * from {} WHERE ip='{}' AND port='{}'".format(self.agent_table, ip, port)
        gets = self.execute_sql_command(sql_command)
        result = True if gets else False
        return result

    def is_exist_slot(self, name):
        sql_command = "SELECT * from {} WHERE name='{}'".format(self.slot_table, name)
        gets = self.execute_sql_command(sql_command)
        result = True if gets else False
        return result

    def update_exist_agent(self, agent):
        str_date = "`os`='{}',platform='{}'".format(agent["os"], agent["platform"])
        cmd = "UPDATE {} SET {} WHERE ip='{}' AND port='{}'".format(self.agent_table, str_date,
                                                                     agent["ip"], agent["port"])
        self.cursor.execute(cmd)
        self.conn.commit()

    def create_new_agent(self, agent):
        self.insert_to_table(self.agent_table,
                             name="{}:{}".format(agent["ip"], agent["port"]),
                             ip=agent["ip"],
                             port=agent["port"],
                             os=agent["os"],
                             platform=agent["platform"])

    def get_agent_related_slots(self, agent):
        cmd = "SELECT * FROM {} where agent='{}'".format(self.slot_table, agent)
        result = self.execute_sql_command(cmd)
        return result


def update_agent(func):
    def func_wrapper(*args, **kwargs):
        agent = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.update_agent(agent)
        except Exception as all_exception:
            log.ERR(all_exception)
        return agent
    return func_wrapper


def update_slot(func):
    def func_wrapper(*args, **kwargs):
        slot_id, slot = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.update_slot(slot_id, slot)
        except Exception as all_exception:
            log.ERR(all_exception)
        return slot
    return func_wrapper

#
# if __name__ == '__main__':
#     dutdb = DutDatabase()
#     agent = {
#         "name": "172.29.128.105:5001",
#         "ip": "172.29.128.105",
#         "port": 5001,
#         "os": "linux",
#         "platform": "perses"
#     }
#
#     slot = {
#         "name": "slot3",
#         "config_name": "oakgate_24_0040",
#         "slot": "0040",
#         "vendor": "new_cnexlabs",
#         "fw_version": "new_PP_10.0.0",
#         "commit": "new_cfef012dw",
#         "ise/sed": "new_sed",
#         "sn": "new_sn0010011002",
#         "cap": "new_2600000",
#         "bb": "new_low bb",
#         "max_ec": "new_120000",
#         "status": "1",
#         "agent": "172.29.129.143:5000"
#
#     }
#
#     dutdb.create_new_agent(agent)
