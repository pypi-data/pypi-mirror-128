import sys
import logging
import traceback

class Logger():

    def __init__(self):
        # 1. 创建logger和handler
        logger = logging.getLogger("kw")
        stream_handler = logging.StreamHandler()
        # file_handler = logging.FileHandler(filename=f"{FILE_PATH_FOR_HOME}/log/test.log")

        # 2. 设置level
            # DEBUG, INFO, WARNING, ERROR, CRITICAL (分别是10, 20, 30, 40, 50)
        logger.setLevel(logging.DEBUG) # 指的是: 最低能支持什么级别的打印输出
        # logger.setLevel(logging.WARNING) # 指的是: 最低能支持什么级别的打印输出
        stream_handler.setLevel(logging.DEBUG)
        # file_handler.setLevel(logging.WARNING)

        # 3. 设置log的输出格式
        # formatter = logging.Formatter("%(asctime)s [%(levelname)s]:  %(message)s") # 其他格式见上面的url
        formatter = logging.Formatter(">>> [%(asctime)s] %(message)s") # 其他格式见上面的url
        stream_handler.setFormatter(formatter)
        # file_handler.setFormatter(formatter)

        # 4. 把handler添加进logger
        logger.addHandler(stream_handler)
        # logger.addHandler(file_handler)

        self.logger = logger


    def _log(self, msg_header, *args, **kwargs):
        _log_msg = msg_header
        for l in args:
            if type(l) == tuple:
                ps = str(l)
            else:
                try:
                    ps = "%r" % l
                except:
                    ps = str(l)
            if type(l) == str:
                _log_msg += ps[1:-1] + " "
            else:
                _log_msg += ps + " "
        if len(kwargs) > 0:
            _log_msg += str(kwargs)
        return _log_msg


    def _log_msg_header(self, *args, **kwargs):
        """Fetch log message header.
        """
        cls_name = ""
        func_name = sys._getframe().f_back.f_back.f_code.co_name
        try:
            _caller = kwargs.get("caller", None)
            if _caller:
                if not hasattr(_caller, "__name__"):
                    _caller = _caller.__class__
                cls_name = _caller.__name__
                del kwargs["caller"]
        except:
            pass
        finally:
            msg_header = "[{cls_name}.{func_name}]:  ".format(cls_name=cls_name, func_name=func_name)
            return msg_header, kwargs


    def debug(self, *args, **kwargs):
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.debug("[DEBUG] " + self._log(msg_header, *args, **kwargs))


    def info(self, *args, **kwargs):
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.info("[INFO] " + self._log(msg_header, *args, **kwargs))


    def warn(self, *args, **kwargs):
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.warn("[WARN] " + self._log(msg_header, *args, **kwargs))


    def warning(self, *args, **kwargs):
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.warning("[WARNING] " + self._log(msg_header, *args, **kwargs))


    def error(self, *args, **kwargs):
        self.logger.error("[ERROR] " + ">"*88)
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.error("[ERROR] " + self._log(msg_header, *args, **kwargs))
        self.logger.error("[ERROR] " + "<"*88)


    def exception(self, *args, **kwargs):
        "封装过的exception: 无需传参, 也会自动打印捕获到的异常"
        self.logger.error("[EXCEPTION] " + ">"*88)
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.error("[EXCEPTION] " + self._log(msg_header, *args, **kwargs))
        e = traceback.format_exc(limit=10)
        self.logger.error("[EXCEPTION] " + e)
        self.logger.error("[EXCEPTION] " + "<"*88)


    def critical(self, *args, **kwargs):
        "封装过的exception: 无需传参, 也会自动打印捕获到的异常; 并且继续raise抛出异常"
        print("\n")
        self.logger.critical("[CRITICAL] " + ">"*88)
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.critical("[CRITICAL] " + self._log(msg_header, *args, **kwargs))
        e = traceback.format_exc(limit=10)
        self.logger.critical("[CRITICAL] " + e)
        self.logger.critical("[CRITICAL] " + "<"*88)
        print("\n")
        raise Exception(e)


    def tmp(self, *args, **kwargs):
        self.logger.critical("[TMP] " + "------------------->>")
        msg_header, kwargs = self._log_msg_header(*args, **kwargs)
        self.logger.critical("[TMP] " + self._log(msg_header, *args, **kwargs))
        self.logger.critical("[TMP] " + "<<-------------------")


    def setLevel(self, *args):
        self.logger.setLevel(*args)



def _get_logger():
    logger = Logger()
    return logger


logger = Logger()


if __name__ == "__main__":
    logger.debug(999, caller=99)
    logger.info(999, caller=99)
    logger.warning(999, caller=99)
    logger.error(999, caller=99)
    logger.exception(999, caller=99)
    logger.tmp(999, caller=99)
    logger.critical(999, caller=99)
