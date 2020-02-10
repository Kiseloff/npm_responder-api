import datetime


def log(file, msg, logtime=True, output=False):
    """
    Log MSG to file

    :param str file: path to log file
    :param str msg: message to log
    :param bool logtime: add time to MSG
    :param output: send MSG to console
    """
    if logtime:
        msg = ' --- '.join([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg.lstrip()])
    if output:
        print(msg)

    with open(file, 'a') as f:
        f.write(msg + '\n')
