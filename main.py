#     -*-    coding: utf-8   -*-
# @File     :       main.py
# @Time     :       2023/3/17 22:47
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

from wcferry import Wcf
import signal  # 处理特殊信号
from robot import Robot


def weather_report(robot: Robot) -> None:
    """
    Send weather forecasts
    """
    # 获取接收人
    receivers = ["filehelper"]

    # 获取天气
    resp = "这是天气预报"

    for i in receivers:
        # 发送消息
        robot.send_text_msg(resp, i)
        # 发信息并且@所有人
        # robot.sendImageMsg(resp, i, "nofity@all")


def main():
    # 运行日志
    wcf = Wcf(debug=True)

    def clean_all(sig, frame):
        wcf.cleanup()  # 退出前清理环境
        exit(0)

    signal.signal(signal.SIGINT, clean_all)

    robot = Robot(wcf)
    robot.LOG.info("----正在启动机器人----")

    # 机器人启动后发送测试消息
    robot.send_text_msg("机器人启动成功！", "filehelper")

    # 接收消息
    robot.enable_receive_message_service()

    # 每天7点定时发送天气预报
    robot.on_every_time('07:00', weather_report, robot=robot)

    # 让机器人一直跑
    robot.keep_running_and_block_the_process()


if __name__ == "__main__":
    main()
