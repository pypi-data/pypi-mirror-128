"""
默认打印颜色
"""
print_color = True


def debug(msg: str, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    log(msg, level="DEBUG")


def info(msg: str, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    log(msg, level="INFO")


def warn(msg: str, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    log(msg, level="WARN")


def error(msg: str, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    log(msg, level="ERROR")


def success(msg: str, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    log(msg, level="OK")


def log(msg, level: str = "INFO", color: bool = None):
    """
    打印日志
    :param msg: 消息
    :param level: 自定义日志等级
    :param color: 是否打印颜色（TRUE/FALSE）
    :return:
    """
    import datetime, os, threading, sys
    level = level.upper()
    pid = os.getpid()
    datetimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    pidStr = fcolor(pid, fg=35)
    levelStr = fcolor("%5s" % level, m=1)
    threadName = threading.currentThread().getName().lower()

    f = sys._getframe().f_back
    fileName = os.path.basename(f.f_code.co_filename)
    lineNo = f.f_lineno
    methodName = os.path.basename(f.f_code.co_name)
    if hasattr(f.f_back, 'f_code'):
        f = f.f_back
        fileName = os.path.basename(f.f_code.co_filename)
        lineNo = f.f_lineno
        methodName = os.path.basename(f.f_code.co_name)

    if methodName == '<module>':
        methodName = ''

    colorMsg = msg
    if level == 'ERROR' or level == 'FAIL':
        colorMsg = fcolor(msg, fg=31)
    if level == 'WARN':
        colorMsg = fcolor(msg, fg=33)
    if level == 'OK' or level == 'SUCCESS':
        colorMsg = fcolor(msg, fg=32)
    if level == 'DEBUG':
        colorMsg = fcolor(msg, fg=37)

    if color is None:
        color = print_color
    if color:
        colorLog = "%s %s %s <%s> - [%s:%s:%s] : %s" % (
            datetimeStr, levelStr, pidStr, fcolor(threadName, fg=34), fcolor(fileName, fg=36), methodName, lineNo,
            colorMsg)
        print(colorLog)
    else:
        log = "%s %5s %s <%s> - [%s:%s:%s] : %s" % (
            datetimeStr, level, pid, threadName, fileName, methodName, lineNo, msg)
        print(log)


def fcolor(msg, m=0, fg=None, bg=None):
    """
    格式化颜色字符串
    :param msg: 文本下次
    :param m: 模式
        0：默认，1：高亮显示，4：下划线，5：闪烁，7：反白显示，8：不可见
    :param fg: 前置色
    :param bg: 背景色
            30	40	黑色
            31	41	红色
            32	42	绿色
            33	43	黄色
            34	44	蓝色
            35	45	紫红色
            36	46	青蓝色
            37	47	白色
    :return:
    """
    if fg and bg:
        return f"\033[{m};{fg};{bg}m{msg}\033[m"
    elif fg or bg:
        return f"\033[{m};{fg or bg}m{msg}\033[m"
    else:
        return f"\033[{m}m{msg}\033[m"