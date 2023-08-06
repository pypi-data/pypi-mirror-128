import logging
import platform
from pathlib import Path


class Log(object):

    def __init__(self, name="logger", console_level=logging.INFO, file_level=logging.INFO,
                 log_fmt="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)s | %(message)s",log_dir=""):
        """
        Log 类初始化函数
        :param name: logger的名称，默认值为：caterpillar_common
        :param console_level: 终端日志级别，默认值为logging.INFO
        :param file_level: 日志文件中的日志级别，默认为loging.INFO
        :param log_fmt: 日志打印的格式，默认为 %(asctime)s | %(levelname)s | %(pathname)s:%(lineno)s | %(message)s
        """
        self.__name = name
        self.__console_level = console_level
        self.__file_level = file_level
        self.__log_fmt = log_fmt
        if log_dir:
            self.__log_dir=log_dir
            self.__log_file=f"{self.__log_dir}/{self.__name}.log"
        else:
            if platform.system() == "Linux":
                self.__log_file = f"/var/log/{self.__name}/{self.__name}.log"
                self.__log_dir = f"/var/log/{self.__name}"
            else:
                self.__log_file = Path(__file__).resolve().parent.parent.parent / f"logs/{self.__name}.log"
                self.__log_dir = Path(__file__).resolve().parent.parent.parent / "logs"


        if not Path(self.__log_dir).exists():
            Path(self.__log_dir).mkdir(parents=True, exist_ok=True)

        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(logging.DEBUG)
        self.__console_handler = logging.StreamHandler()
        self.__console_handler.setLevel(self.__console_level)
        self.__file_handler = logging.FileHandler(filename=self.__log_file)
        self.__file_handler.setLevel(self.__file_level)
        self.__formatter = logging.Formatter(fmt=self.__log_fmt)
        self.__console_handler.setFormatter(self.__formatter)
        self.__file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__console_handler)
        self.__logger.addHandler(self.__file_handler)

logger=Log("caterpillar_log")
