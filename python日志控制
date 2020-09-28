# coding=utf-8
import logging
import datetime
import os


CONSOLE = True
LEVEL = "DEBUG"
# log/2020-09/2020-09-27_APPLICATION_NAME.log
APPLICATION_NAME = "APPLICATION_NAME"


# 只生成GBK的日志文件
class RecordLog:

    def __init__(self):
        """
        1、控制日志是否在控制台中打印
        2、控制日志输出的级别
        """
        # 设置是否控制台打印
        self._console = CONSOLE
        # 等级字典
        self._level_dict = {'DEBUG':1,'INFO':2,'WARNING':3,'ERROR':4,'CRITICAL':5}
        # 设置当前支持的日志等级
        self._current_level_num = self._level_dict[LEVEL]

    def get_log_file_name(self,):
        """
        创建日志文件夹，创建或调用日志文件,日志存储
        :return: log/log_folder(月份)/log_file（每天的log）
        """
        now = str(datetime.datetime.now())
        log_folder = now[:7]
        log_file = now[:10] + "_" + APPLICATION_NAME + ".log"
        if os.path.exists("log/" + log_folder):
            pass
        else:
            os.makedirs("log/" + log_folder)
        return "log/" + log_folder + "/" + log_file

    def log_content(self, content='开始记录',level="DEBUG"):
        """
        记录日志
        :param content: 记录的内容
        :param level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        :return:
        """
        LOG_FILE_NAME = self.get_log_file_name()
        now1 = datetime.datetime.now()
        now_date = now1.strftime("%Y-%m-%d-%H:%M:%S")
        text = " %s %s -- %s" % (level, now_date, content)
        if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            level_num = self._level_dict[level]
            # 控制台输出
            if self._console:
                print(text)

            logger = logging.getLogger()
            fh = logging.FileHandler(filename=LOG_FILE_NAME, encoding="utf-8", mode="a")
            # formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")
            # fh.setFormatter(formatter)
            logger.addHandler(fh)
            # 设置日志等级
            if "DEBUG" == level and level_num >= self._current_level_num:
                logger.setLevel(logging.DEBUG)
            elif "INFO" == level and level_num >= self._current_level_num:
                logger.setLevel(logging.INFO)
            elif "WARNING" == level and level_num >= self._current_level_num:
                logger.setLevel(logging.WARNING)
            elif "ERROR" == level and level_num >= self._current_level_num:
                logger.setLevel(logging.ERROR)
            else:
                logger.setLevel(logging.CRITICAL)
            logger.info(text)
        else:
            raise Exception('日志等级传参错误： %s ; 正确格式为：DEBUG, INFO, WARNING, ERROR, CRITICAL'%level)


if __name__ == '__main__':
    #
    log = RecordLog()
    log.log_content(level='DEBUG')
