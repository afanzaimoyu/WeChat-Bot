#     -*-    coding: utf-8   -*-
# @File     :       my_config.py
# @Time     :       2023/3/18 0:50
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

import os
import json
import logging.config


class Config:
    """
    read the configuration file
    """

    def __init__(self) -> None:
        """
        read the configuration file
        """
        self.initial_prompt = None
        self.max_token_length = None
        self.timeout = None
        self.Proxies = None
        self.CHAT_KEY = None
        self.GROUPS = None
        self.reload()

    def __repr__(self):
        print(self.initial_prompt, self.max_token_length, self.timeout, self.Proxies, self.CHAT_KEY, self.GROUPS)

    def load_config(self) -> dict:
        """
        read profile information
        :return: json_config:  profile information
        """
        name = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(f"{name}/config.json", mode='r', encoding='utf-8') as f:
                json_config = json.load(f)
        except FileExistsError:
            with open(f"{name}/config.json.template", mode='r', encoding='utf-8') as f:
                json_config = json.load(f)
                with open(f"{name}/config.json", mode='w+', encoding='utf-8') as f1:
                    json.dump(json_config, f1, indent=2)

        return json_config

    def reload(self) -> None:
        """
        read profile information
        """
        json_config = self.load_config()
        logging.config.dictConfig(json_config['logging'])
        self.CHAT_KEY = json_config['chatgpt']['key']
        self.GROUPS = json_config['groups']['enable']
        self.Proxies = json_config['chatgpt']['proxies']
        self.timeout = json_config['chatgpt']['timeout']
        self.max_token_length = json_config['chatgpt']['max_token_length']
        self.initial_prompt = json_config['chatgpt']['initial_prompt']


if __name__ == '__main__':
    config = Config()
    print(config)
