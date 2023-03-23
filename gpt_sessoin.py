#     -*-    coding: utf-8   -*-
# @File     :       gpt_sessoin.py
# @Time     :       2023/3/18 15:58
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

from gpt_api import GptThread
import logging


class session:
    def __init__(self, config):
        self.cont = 0
        self.LOG = logging.getLogger("session")
        self.c = config
        self.chat = GptThread(api_key=self.c.CHAT_KEY, proxies=self.c.Proxies, time_out=self.c.timeout,
                              max_token=self.c.max_token, initial_prompt=self.c.initial_prompt)

    def __repr__(self):
        print(self.cont, 'cont')

    def ask(self, question):
        print(self.cont, 'cont')
        if self.cont >= 7:
            self.chat.add_user_contet('请以最精简的话语总结我们的对话，100字以内')
            res = self.chat.get_resp()
            now_sys = self.chat.msg[0]['content']
            self.chat.add_system_content(now_sys)
            self.chat.add_bot_content(res)
            self.cont = 0
            resp = "哎呀，脑袋不够用了呢，总感觉忘了什么事似的，真奇怪QAQ,麻烦你再问一遍吧"
        else:
            self.chat.add_user_contet(question)
            resp = self.chat.get_resp()
            self.chat.add_bot_content(resp)
            self.cont += 1
        self.LOG.info(f"现在为第{self.cont}轮，聊天内容为{self.chat.msg}")
        return resp

    def now_init_session(self):
        self.cont = 0
        a = self.chat.msg[0]['content']
        self.chat.add_system_content(a)
        self.LOG.info(f"初始化session，现在为第{self.cont}次")
        return "已重置本轮对话,让我们重新开始吧"

    def start_session(self):
        self.cont = 0
        self.chat.reset_msg()
        a = self.chat.msg[0]['content']
        return f"已重置本轮对话,让我们重新开始吧,现在的人设是：{a}"

    def reserve_session(self, question):
        self.cont = 0
        self.chat.add_system_content(question)
        return f"我现在的人设是{question}让我们开始聊天吧吧"

    def get_now_system(self):
        return self.chat.msg[0]['content']
