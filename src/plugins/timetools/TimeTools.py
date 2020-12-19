# -*- coding: utf-8 -*-
# create by yihui 10:51 19/10/9
import datetime as datetime

MONTH = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

NOVEL_MONTH = {
    'Dec': 12,
    'Nov': 11,
    'Oct': 10,
    'Sep': 9,
    'Aug': 8,
    'Jul': 7,
    'Jun': 6,
    'May': 5,
    'Apr': 4,
    'Mar': 3,
    'Feb': 2,
    'Jan': 1,
}


def entime2str(now: str):
    """
    英文日期转换
    Monday, February 10, 2020 10:42 PM
    :param now:
    :return:
    """
    cell = now.split(',')
    month_day = cell[1].strip().split(' ')
    month = MONTH.get(month_day[0])
    day = int(month_day[1].strip())

    year_time = cell[2].strip().split(' ')
    year = int(year_time[0].strip())

    hour_minutes = year_time[1].strip().split(':')
    hour = int(hour_minutes[0].strip())
    if year_time[2].strip().lower() == 'pm' and hour != 12:
        # pm 如果hour为12点，那么啥都不干
        hour = int(hour_minutes[0].strip()) + 12
    minutes = int(hour_minutes[1].strip())
    return f"{year}-{month}-{day} {hour}:{minutes}:00"


def novel_time2str(now: str):
    cells = now.split('-')
    month = NOVEL_MONTH[cells[0]]
    day = cells[1]
    year = cells[2]

    hour = 0
    minutes = 0
    return f"{year}-{month}-{day} {hour}:{minutes}:00"


def novel_desc_time2str(now: str):
    day_info, hour_info = now.split(' ')
    cells = day_info.split('-')
    month = NOVEL_MONTH[cells[1].strip()]
    day = cells[0].strip()
    year = cells[2].strip()

    cells = hour_info.split(':')
    hour = cells[0].strip()
    minutes = cells[1].strip()
    return f"{year}-{month}-{day} {hour}:{minutes}:00"


def now_timestamp():
    """
    获取当前时间戳，ms单位
    :return:
    """
    return int(datetime.datetime.now().timestamp() * 1000)


def str2date(now: str, format_style: str):
    """
    字符串转日期
    :param now:
    :param format_style:
    :return:
    """
    return datetime.datetime.strptime(now, format_style)


def str2timestamp(now: str, format_style: str = '%Y-%m-%d %H:%M:%S'):
    """
    字符串转ms时间戳
    :param now:
    :param format_style:
    :return:
    """
    date = str2date(now, format_style)
    return int(date.timestamp() * 1000)


def timestamp2date(now: int):
    """
    时间戳转日期
    :param now: ms单位的时间戳
    :return:
    """
    return datetime.datetime.fromtimestamp(now / 1000)


def timestamp2str(now: int, format_style: str = '%Y-%m-%d %H:%M:%S'):
    date = timestamp2date(now)
    return date2str(date, format_style)


def date2str(now: datetime.datetime, format_style: str = '%Y-%m-%d %H:%M:%S'):
    return now.strftime(format_style)


def to_quarter_start_day(now: datetime.datetime):
    """
    将时间转换为对应季度最后一个月的月初
    :param now:
    :return:
    """
    m = now.month
    if m <= 3:
        return datetime.datetime(now.year, 3, 1)
    elif m <= 6:
        return datetime.datetime(now.year, 6, 1)
    elif m <= 9:
        return datetime.datetime(now.year, 9, 1)
    elif m <= 12:
        return datetime.datetime(now.year, 12, 1)


def to_this_friday(now: datetime.datetime):
    """
    转换为本周五
    :param now:
    :return:
    """
    return now + datetime.timedelta(days=4 - now.weekday())


def to_next_friday(now: datetime.datetime):
    """
    转换为下周五
    :param now:
    :return:
    """
    return now + datetime.timedelta(days=7 + 4 - now.weekday())


def to_this_monday(now: datetime.datetime):
    """
    跳转到本周周一
    :param now:
    :return:
    """
    return now + datetime.timedelta(days=-now.weekday())


def to_month_first_day(now: datetime.datetime):
    """
    转到本月第一天
    :param now:
    :return:
    """
    now = now.replace(day=1)
    return now


def to_next_month_first_day(now: datetime.datetime):
    """
    获取下月的第一天
    :param now:
    :return:
    """
    now = to_month_first_day(now)
    # 跳转到下一个月
    next = now + datetime.timedelta(days=31)
    return to_month_first_day(next)


def to_month_last_friday(now: datetime.datetime):
    """
    获取这个月的最后一个星期五
    :param now:
    :return:
    """
    # 获取本月最后一天
    next = now + datetime.timedelta(days=31)
    next = next.replace(day=1)
    now = next + datetime.timedelta(days=-1)

    if now.weekday() == 4:
        # 最后天正好周五
        return now
    elif now.weekday() > 4:
        # 最后一天大于周五:
        return now + datetime.timedelta(days=4 - now.weekday())
    else:
        # 最后一天小于周五，则取前一周
        return now + datetime.timedelta(days=-7 + 4 - now.weekday())
