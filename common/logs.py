import yaml
import logging

def get_log_level(name):
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR
    }
    try:
        return levels[name]
    except KeyError:
        raise ValueError("Invalid log level name {}. Choose one of {}.".format(
            name, ", ".join(levels.keys())
        ))

def get_logger(logName, fileName, level):
    "Gets a preconfigured logger"
    log = logging.getLogger(logName)
    log.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh = logging.FileHandler(fileName)
    sh = logging.StreamHandler()
    for h in [fh, sh]:
        h.setLevel(level)
        h.setFormatter(formatter)
        log.addHandler(h)
    return log
