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
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from wcferry import Wcf

from my_config import Config
from job_all import Job
from gpt_sessoin import session
from test import Weather
from baidu.speak import Baidu


class Robot(Job):
    """
    personalized bots
    """

    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.config = Config()
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allPeople = self.getall_people()
        self.session = session(config=self.config)
        self.wt = Weather()
        self.baidu = Baidu()

    def enable_receive_message_service(self) -> None:
        """
        启动接收消息的服务
        """
        self.wcf.enable_recv_msg(self.action_msg)

    def action_msg(self, msg: Wcf.WxMsg):
        """
        接收到消息的处理
        :param msg: 微信消息体
        """
        try:
            self.LOG.info(msg)
            self.various_methods(msg)
        except Exception as e:

            self.LOG.error(f'出现错误，接收消息出粗：{e}')

    def various_methods(self, msg: Wcf.WxMsg) -> None:
        """
        接收到消息的时候会调用这个方法，不调用，打印原始消息
        群号: msg.roomid 微信ID: msg.sender 消息内容: msg.content
        :param msg: 微信消息体 包含以上信息
        """

        if msg.from_group():  # 群聊消息
            self.from_group_msg(msg)
        else:
            if msg.type == 37:  # 好友请求
                self.from_friend_request(msg)
            elif msg.type == 10000:  # 系统消息
                self.from_system_info(msg)
            elif msg.type == 0x01:  # 文本消息
                self.from_text_msg(msg)

    def from_group_msg(self, msg: Wcf.WxMsg) -> None:
        """
        处理群聊消息
        :param msg: 微信消息体
        """
        if msg.roomid not in self.config.GROUPS:  # 不在允许的配置里面
            self.LOG.info(f'收到群聊消息，但是{msg.roomid}没有在{self.config.GROUPS}中配置，不处理\n')
            return
        elif msg.is_at(self.wxid):  # 被@
            self.at_me(msg)
        else:
            return

    def from_friend_request(self, msg: Wcf.WxMsg) -> None:
        """
        处理好友请求
        :param msg: 微信消息体
        """
        self.auto_accept_friend_request(msg)

    def from_system_info(self, msg: Wcf.WxMsg) -> None:
        """
        处理系统消息
        :param msg: 微信消息体
        """
        self.say_hi_to_new_friend(msg)

    def from_text_msg(self, msg: Wcf.WxMsg) -> None:
        """
        处理文本消息
        :param msg:  微信消息体
        """
        if msg.from_self() and msg.content == '更新':
            self.config.reload()
            self.LOG.info('更新配置成功')
        else:
            self.get_chat_gpt(msg)

    def at_me(self, msg: Wcf.WxMsg) -> bool:
        """
        处理被@的消息
        :param msg: 微信消息结构体
        :return: 处理状态， True为处理成功， False为处理失败
        """
        question = re.sub(r"@.*?[\u2005|\s]", "", msg.content).strip()

        if question == '?' or question == '？':
            resp = '''
        使用手册：
            @ 我 而不是复制哦
            0. ? 查看帮助
            1. 直接跟我聊天
            2. /init 重置对话,回归初始人设
            3. /remove 重置对话
            4. /reserve+初始人物设定 创建新的人格 
            5. /prompt 查看当前人设
            6. /weather +地点 查看天气
            7. /sing 文本转语音
            问题： i:现在几个群一起聊天信息会串起来，有空再改
                ii:长字数的回答后面会卡死。。。。。。
            '''
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True

        if '/prompt' == question:
            resp = self.session.get_now_system()
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True
        if '/weather' in question:
            q = re.sub(r"/weather", "", question).strip()
            resp = self.wt.get_weather(q)
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True

        if '/reserve' in question:
            q = re.sub(r"/reserve", "", question).strip()
            resp = self.session.reserve_session(q)
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True

        if '/init' in question:
            print(question, "重置对话")
            resp = self.session.start_session()
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True

        if '/remove' == question:
            resp = self.session.now_init_session()
            at_lists = msg.sender
            self.send_text_msg(resp, msg.roomid, at_lists)
            return True

        if '/sing' in question:
            q = re.sub(r"/sing", "", question).strip()
            resp = self.session.ask(q+'，请少于1024GBK字节')
            self.baidu.speak(resp)
            a = at_lists = msg.sender
            if a:
                self.LOG.info("----语音已生成----")
                self.wcf.send_file('./baidu/audio.mp3', msg.roomid)
                self.send_text_msg(resp, msg.roomid, at_lists)
                return True
            else:
                self.send_text_msg("生成失败", msg.roomid, at_lists)
        else:
            return self.get_chat_gpt(msg)

    def get_chat_gpt(self, msg: Wcf.WxMsg) -> bool:
        """
        获取聊天结构体中的gpt模型
        :param msg: 微信消息结构体
        :return: 处理状态， True为处理成功， False为处理失败
        """
        question = re.sub(r"@.*?[\u2005|\s]", "", msg.content)
        resp = self.session.ask(question)
        print(question, 'question')
        print(resp, 'resp')
        if resp:
            receiver = msg.roomid if msg.from_group() else msg.sender
            at_lists = ""
            if msg.from_group():
                at_lists = msg.sender
            self.send_text_msg(resp, receiver, at_lists)
            return True
        else:
            self.LOG.error("---无法从ChatGPT获得答案---")
            return False

    def send_text_msg(self, msg: str, receiver: str, at_lists: str = '') -> None:
        """
        发送文本消息
        :param msg: 消息内容
        :param receiver: 接收人的wxid或者群roomid
        :param at_lists: 要@的人的wxid列表，@所有人为：nofity@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        wxids = at_lists.split(",") if at_lists else []
        ats = ''.join([f' @{self.allPeople.get(wxid, "")}' for wxid in wxids])
        self.LOG.info(f"To {receiver}: {msg}{ats}")
        self.wcf.send_text(f"{msg}{ats}", receiver, at_lists)

    def getall_people(self) -> dict:
        """
        获取联系人（包括好友、公众号、服务号、群成员……）
        格式: {"wxid": "NickName"}
        """
        contacts = self.wcf.query_sql(
            "MicroMsg.db", "SELECT UserName, NickName FROM Contact;")
        return {contact["UserName"]: contact["NickName"]
                for contact in contacts}

    def auto_accept_friend_request(self, msg: Wcf.WxMsg):
        """
        自动接受好友请求
        :param msg: 微信消息结构体
        """
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            self.wcf.accept_new_friend(v3, v4)

        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")

    def say_hi_to_new_friend(self, msg):
        """
        接收好友请求后自动发送消息
        :param msg:
        """
        nick_name = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
        if nick_name:
            # 添加了好友，更新好友列表
            self.allPeople = nick_name[0]
            self.send_text_msg(f"Hi {nick_name[0]}，我自动通过了你的好友请求。", msg.sender)

    def keep_running_and_block_the_process(self):
        """
        保持机器人运行，不让进程退出
        """
        while True:
            self.run_pending_jobs()
            time.sleep(1)
