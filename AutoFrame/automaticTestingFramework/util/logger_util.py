import logging
from automaticTestingFramework.conf import env_conf


class Logger:
    """ 日志操作 """
    _logger_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, log_name, file_name, logger_level, stream_level='info', file_level='warning'):
        self.log_name = log_name
        self.file_name = file_name
        self.logger_level = self._logger_level.get(logger_level, 'debug')
        self.stream_level = self._logger_level.get(stream_level, 'info')
        self.file_level = self._logger_level.get(file_level, 'warning')
        # 创建日志对象
        self.logger = logging.getLogger(self.log_name)
        # 设置日志级别
        self.logger.setLevel(self.logger_level)
        if not self.logger.handlers:
            # 设置日志输出流
            f_stream = logging.StreamHandler()
            f_file = logging.FileHandler(self.file_name, encoding='utf-8')
            # 设置输出流级别
            f_stream.setLevel(self.stream_level)
            f_file.setLevel(self.file_level)
            # 设置日志输出格式
            formatter = logging.Formatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
            f_stream.setFormatter(formatter)
            f_file.setFormatter(formatter)
            self.logger.addHandler(f_stream)
            self.logger.addHandler(f_file)

    @property
    def get_logger(self):
        return self.logger


def logger(log_name='接口测试'):
    return Logger(
        log_name=log_name,
        logger_level=env_conf.LOG_LEVEL,
        file_name=env_conf.LOG_FILE_NAME,
        stream_level=env_conf.LOG_STREAM_LEVEL,
        file_level=env_conf.LOG_FILE_LEVEL
    ).get_logger


logger = logger('demo')

if __name__ == '__main__':

    logger.debug('11111')
    logger.info('22222')
    logger.warning('33333')
