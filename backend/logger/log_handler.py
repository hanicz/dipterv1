from utils import log_level, LEVEL


def log_message(level,message):

    if log_level.value <= level.value:
        with open('server_log.log', "a") as f:
            f.write(message + '\n')
