#     -*-    coding: utf-8   -*-
# @File     :       speak.py
# @Time     :       2023/3/23 22:06
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE
from aip import AipSpeech
# 百度ai接口
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

class Baidu:
    def __init__(self):
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def speak(self, question):
        result = self.client.synthesis(f'{question}', 'zh', 1, {
            'vol': 5,
            'per': 0,
        })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open('./baidu/audio.mp3', 'wb') as f:
                f.write(result)
                return True
        else:
            return False


if __name__ == '__main__':
    Baidu().speak('你好')
