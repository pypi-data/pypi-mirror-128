import time
from datetime import datetime, timedelta
import pytz

"""
1、时间戳转当前时间
2、utc时间转本地时间
3、数据库获取的时间转换为指定格式
"""


def timestamp_to_now(time_stamp):
    """
    时间戳 转 当前时间
    :param time_stamp: 例:1634044793.5933821
    :return: 例:2021-10-12 21:19:53
    """
    time_stamp = float(time_stamp)
    now_time = time.localtime(time_stamp)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now_time)
    return now_time


def now_to_timestamp(now_time):
    """
    当前时间 转 时间戳
    :return:
    :param now_time:  例:2021-10-12 21:34:54
    :return: 例:1634045694.0
    """
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = time.mktime(timeArray)
    return time_stamp


def utc_local_time(utc_str):
    """utc时间转本地时间
    :param now_time:  utc_str (string or time): 转datetime，并加8得到本地实际 2021-10-12 22:01:52
    :return: 例:2021-10-12 22:01:52
    Args:
        utc_str (string or time): 转datetime，并加8得到本地实际 2021-07-30T05:56:00Z
    """
    if not isinstance(utc_str, str):
        utc_str = utc_str.strftime("%Y-%m-%d %H:%M:%S")
    try:
        utc_time = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S.%f+00:00")
    except ValueError:
        utc_time = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
    shanghai_time = utc_time + timedelta(hours=8)
    now_time = datetime(shanghai_time.year, shanghai_time.month, shanghai_time.day, shanghai_time.hour,
                        shanghai_time.minute,
                        shanghai_time.second)
    return now_time
