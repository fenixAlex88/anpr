import logging
from logging.handlers import RotatingFileHandler
import time

class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        """Форматирование времени с миллисекундами."""
        ct = self.converter(record.created)
        t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
        s = "%s,%03d" % (t, record.msecs)
        return s

def setup_logger(name, log_file, level=logging.INFO):
    """Настройка логера с ротацией файлов."""
    # Создаем обработчик ротации файлов
    handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    handler.setLevel(level)

    # Формат логов
    formatter = MillisecondFormatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Настройка логера
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger