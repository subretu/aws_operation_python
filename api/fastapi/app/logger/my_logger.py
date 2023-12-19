import logging
from pythonjsonlogger import jsonlogger
import datetime
from pytz import timezone
from functools import wraps
import inspect


class JsonFormatter(jsonlogger.JsonFormatter):
    def parse(self):
        return [
            "level",
            "funcName",
            "process",
            "timestamp",
            "name",
            "message",
            "stack_info",
        ]

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.datetime.now(timezone("Asia/Tokyo")).strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            )
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def set_logger(module_name):
    # loggerの設定
    logger = logging.getLogger(module_name)
    # ログが重複して出ないようクリア
    logger.handlers.clear()

    # handkerの設定
    streamHandler = logging.StreamHandler()

    # ログ出力のフォーマッターの設定
    formatter = JsonFormatter()
    streamHandler.setFormatter(formatter)

    # ログレベルの設定
    logger.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)

    # loggerにhanderを追加
    logger.addHandler(streamHandler)

    return logger


def logging_function(logger):
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            func_result = func(*args, **kwargs)
            # loggerで使用するためにfuncに関する情報をdict化
            extra = {
                "real_filename": inspect.getfile(func),
                "real_funcName": func_name,
                "real_lineno": inspect.currentframe().f_back.f_lineno,
                "real_result": func_result,
            }

            logger.info(f"[START] {func_name}", extra=extra)

            try:
                # funcの実行
                return func(*args, **kwargs)
            except Exception as err:
                # funcのエラーハンドリング
                logging.error(err, exc_info=True, extra=extra)
                logging.error(f"[KILLED] {func_name}", extra=extra)
            else:
                logging.info(f"[END] {func_name}", extra=extra)

        return wrapper

    return _decorator
