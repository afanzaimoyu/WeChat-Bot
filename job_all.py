#     -*-    coding: utf-8   -*-
# @File     :       job_all.py
# @Time     :       2023/3/17 23:42
# Author    :       摸鱼呀阿凡
# Version   :       1.0
# Contact   :       f2095522823@gmail.com
# License   :       MIT LICENSE

import time
import schedule
from typing import Any, Callable


class Job:

    def __init__(self) -> None:
        pass

    def on_every_seconds(self, seconds: int, tasks: Callable[..., Any], *args, **kwargs) -> None:
        """
        executed every x seconds
        :param seconds: 时间间隔,  单位秒
        :param tasks: 任务
        :return: None
        """
        schedule.every(seconds).seconds.do(tasks, *args, **kwargs)

    def on_every_minutes(self, minutes: int, tasks: Callable[..., Any], *args, **kwargs) -> None:
        """
        executed every x minutes
        :param minutes: 时间间隔,  单位分钟
        :param tasks: 任务
        :return: None
        """
        schedule.every(minutes).minutes.do(tasks, *args, **kwargs)

    def on_every_hours(self, hours: int, tasks: Callable[..., Any], *args, **kwargs) -> None:
        """
        Performed every x hours
        :param hours: 时间间隔,  单位小时
        :param tasks: 任务
        :return: None
        """
        schedule.every(hours).hours.do(tasks, *args, **kwargs)

    def on_every_days(self, days: int, tasks: Callable[..., Any], *args, **kwargs) -> None:
        """
        performed every x days
        :param days: 时间间隔,  单位天
        :param tasks: 任务
        :return: None
        """
        schedule.every(days).days.do(tasks, *args, **kwargs)

    def on_every_time(self, times: str, tasks: Callable[..., Any], *args, **kwargs) -> None:
        """
        executed once a day at x points
        例子: times=["10:30", "10:45", "11:00"]
        :param times: 时间间隔,  格式:
             - For daily jobs -> HH:MM:SS or HH:MM
            - For hourly jobs -> MM:SS or :MM
            - For minute jobs -> :SS
        :param tasks: 任务
        :return: None
        """
        if not isinstance(times, list):
            times = [times]

        for i in times:
            """
            schedule库:
                 every(1) 表示设置任务的重复周期为1，即每隔1天执行一次任务。
                .days 表示选择每隔1天执行任务的单位为天（如果设置为hours，则任务每隔1小时执行一次）。
                .at(i) 表示任务的执行时间是在指定的t时间，例如："09:00"。
                .do(tasks, *args, **kwargs) 表示任务执行的名称和参数。
                 tasks是任务的名称，*args和**kwargs是任务的参数。
            """
            schedule.every(1).day.at(i).do(tasks, *args, **kwargs)

    def run_pending_jobs(self) -> None:
        schedule.run_pending()


if __name__ == '__main__':
    def print_str(s):
        print(s)


    job = Job()
    job.on_every_seconds(1, print_str, "1秒")
    job.on_every_minutes(59, print_str, " 59分钟")
    job.on_every_hours(23, print_str, " 23小时")
    job.on_every_days(1, print_str, " 1天")
    job.on_every_time("10:00", print_str, "每天十点")

    while True:
        job.run_pending_jobs()
        time.sleep(1)
