#     -*-    coding: utf-8   -*-
# @File     :       test.py
# @Time     :       2023/3/20 23:57
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE
import requests
import logging
from fake_useragent import UserAgent


class Weather:
    def __init__(self) -> None:
        """
        初始化Weather类。生成日志记录器Logger、用户代理user_agent以及天气API的URL。
        """
        self.user_agent = UserAgent()
        self.LOG = logging.getLogger("Weather")
        self.url = 'https://zhwnlapi.etouch.cn/Ecalender/weather_mini'

    def get_weather(self, city: str) -> str:
        """
        根据给定城市获取天气。

        Args:
            city: str - 要获取天气的城市。
            headers: dict - 提供要在请求中添加的headers值。默认为空。

        Returns:
            str - 包含给定城市的天气数据的字符串。

        Raises:
            Exception - API返回异常。
        """
        try:
            headers = {
                "User-Agent": self.user_agent.random
            }
            params = {"city": city}
            resp = requests.get(self.url, params=params, headers=headers).json()
            data = resp.get('data', {})

            if not data:
                self.LOG.error(f"No weather data found for {city}")
                return f"No weather data found for {city}"

            today_weather = data['forecast'][0]
            city_name = data.get('city', '')
            today = today_weather['date']
            high, low = today_weather['high'], today_weather['low']
            fengxiang, weather_type = today_weather['fengxiang'], today_weather['type']
            fengli = today_weather['fengli'][9:11] if today_weather['fengli'] else ''
            output = f"今天是{today}，{city_name}的天气情况如下：{high}，{low}，风力: {fengli}，风向: {fengxiang}，空气质量为：{weather_type}"
            self.LOG.info(output)
            return output

        except requests.exceptions.RequestException as e:
            self.LOG.error(f"{e}")
            return f"天气获取失败，请稍后再试"


if __name__ == '__main__':
    weather = Weather()
    a = weather.get_weather("北京")
    print(a)
