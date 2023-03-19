#     -*-    coding: utf-8   -*-
# @File     :       gpt_sessoin.py
# @Time     :       2023/3/18 15:58
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

from gpt_api import GptThread


class session:
    def __init__(self, config):
        self.cont = 0
        self.c = config
        self.chat = GptThread(api_key=self.c.CHAT_KEY, proxies=self.c.Proxies, time_out=self.c.timeout,
                              max_token=self.c.max_token, initial_prompt=self.c.initial_prompt)

    def __repr__(self):
        print(self.cont, 'cont')

    def ask(self, question):
        print(self.cont, 'cont')
        if self.cont >= 10:
            self.chat.add_user_contet('请以最精简的话语总结我们的对话，100字以内')
            res = self.chat.get_resp()
            self.chat.reset_msg()
            self.chat.add_bot_content(res)
            self.cont = 0
            resp = "哎呀，脑袋不够用了呢，总感觉忘了什么事似的，真奇怪QAQ"
        else:
            self.chat.add_user_contet(question)
            resp = self.chat.get_resp()
            self.chat.add_bot_content(resp)
            self.cont += 1

        return resp

    def start_session(self):
        pass
