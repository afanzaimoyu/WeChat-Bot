#     -*-    coding: utf-8   -*-
# @File     :       gpt_api.py
# @Time     :       2023/3/17 20:27
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE
from datetime import datetime

import openai

proxies = {
    'http': 'http://127.0.0.1:proxy',
    'https': 'http://127.0.0.1:proxy'

}
openai.proxy = proxies

api_key = 'your_api_key'
openai.api_key = api_key

MAX_TOKEN_LENGTH = 1024
TIME_OUT = 3

MANAGE_ROLE = 'system'  # 设定助手的行为
BOT_ROLE = 'assistant'  # 当chatGPT忘记了上下文，就可以用来存储先前的响应，给chatGPT提供所需的行为实例
USER_ROLE = 'user'  # 用户输入

initial_prompt = 'your initial prompt'


class GptThread:
    """
    chatgpt
    """

    def __init__(self):
        self.msg = []
        self.reset_msg()

    def a_message_was_received_from_the_api(self):
        """
        create chatgpt with openai
        :return: resp: ChatGPT's reply
        """
        response = []
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.msg,
            temperature=1.0,  # 0-2 越高回答越随机
            max_tokens=MAX_TOKEN_LENGTH,
            timeout=TIME_OUT,
        )
        resp = response['choices'][0]['message']['content']
        return resp

    def get_resp(self, prompt):
        """
        user send a prompt and get a response
        :param prompt: user send a prompt
        :return: resp: ChatGPT's reply(after processing)
        """
        try:
            self.add_user_contet(prompt)
            resp = self.a_message_was_received_from_the_api()
            resp = resp[2:] if resp.startswith("\n\n") else resp
            resp = resp.replace("\n\n", "\n")
            self.add_bot_content(resp)
        except Exception as e:
            resp = ''

        return resp

    def reset_msg(self):
        """
        reset chatgpt msg
        """

        self.msg = [{'role': MANAGE_ROLE, 'content': initial_prompt}]

    def add_bot_content(self, content):
        """
        Add bot content to the chatgpt msg
        :param content: the last round of conversation
        """
        self.msg.append({'role': BOT_ROLE, 'content': content})

    def add_user_contet(self, content):
        """
        Add user content to the chatgpt msg
        :param content: user input
        """
        self.msg.append({'role': USER_ROLE, 'content': content})

    def reset_system_content(self, content):
        """
        Reset system content.
        :param content:  initial system message
        """
        self.msg = [{'role': 'system', 'content': content}]


if __name__ == '__main__':
    gpt_thread = GptThread()
    t1 = datetime.now()
    resp = gpt_thread.get_resp('你好，我是主人')
    t2 = datetime.now()
    print(f'用时{t2 - t1}秒')
    print(resp)
