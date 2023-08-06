import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from tool.device.nvme.nvme import Tahoe
from utils.system import execute


class LinuxNvme(object):

    def __init__(self):
        pass

    @staticmethod
    def get_info(cntid=0):
        driver = Tahoe(cntid=cntid)
        information = driver.get_info()
        return information

    @staticmethod
    def get_linux_nvme_devs():
        dev_list = list()
        control_list = list()
        cmd = "lsblk"
        _, outs = execute(cmd)
        rets = re.findall("(nvme(\d+))n(\d+)", outs, re.DOTALL)
        for item in rets:
            if item[1] not in control_list:
                dev = {"ctrl_id": item[1], "name": item[0]}
                control_list.append(item[1])
                dev_list.append(dev)
        return dev_list
