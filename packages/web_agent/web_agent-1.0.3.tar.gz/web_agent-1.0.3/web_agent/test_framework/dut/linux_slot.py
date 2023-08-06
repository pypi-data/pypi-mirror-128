
from test_framework.database.dut_database import update_slot


class LinuxSlot(object):

    def __init__(self, slot_id, config_name):
        self.slot_id = slot_id
        self.config_name = config_name

    @update_slot
    def refresh(self):
        pass
