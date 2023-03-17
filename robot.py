#     -*-    coding: utf-8   -*-
# @File     :       robot.py
# @Time     :       2023/3/17 23:36
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

import re
import time
import logging
from lxml import etree as ET

from wcferry import Wcf

from my_config import Config
from job_all import Job
from gpt_api import GptThread


class Robot(Job):
    """
    personalized bots
    """

    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.config = Config()
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allPeople = self.getallPeople()
        self.chat = GptThread(self.config.CHAT_KEY)

    def getallPeople(self):
        pass
