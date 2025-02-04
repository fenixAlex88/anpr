import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger_module import setup_logger

# Настройка логгера
logger = setup_logger("ANPR", "anpr_ftp.log")

class ChangeHandler(FileSystemEventHandler):
    """Класс для обработки событий изменения файловой системы."""
    
    def on_modified(self, event):
        if not event.is_directory:  # Игнорируем изменения директорий
            logger.info(f"Изменен файл: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:  # Игнорируем создание директорий
            logger.info(f"Создан файл: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:  # Игнорируем удаление директорий
            logger.info(f"Удален файл: {event.src_path}")

def main():
    path = "/home/o1entry2/"  # Путь к отслеживаемой директории
    logger.info(f"Начинаем наблюдение за директорией: {path}")
    
    # Создаем обработчик событий и наблюдателя
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Остановка наблюдателя по сигналу KeyboardInterrupt.")
        observer.stop()
    except Exception as e:
        logger.error(f"Ошибка в наблюдателе: {e}")
    finally:
        observer.join()
        logger.info("Наблюдатель завершил работу.")

if __name__ == "__main__":
    main()
