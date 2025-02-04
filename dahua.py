from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from logger_module import setup_logger

# Настройка логера
logger = setup_logger("ANPR", "anpr_server.log")

class DahuaANPRHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        # Логирование эндпоинта
        logger.info(f"Запрос на эндпоинт: {self.path}")

        # Вывод заголовков
        logger.info("Заголовки запроса:")
        for header, value in self.headers.items():
            logger.info(f"{header}: {value}")

        # Вывод всех cookie
        if "Cookie" in self.headers:
            cookies = self.headers.get_all("Cookie")
            logger.info("Cookies:")
            for cookie in cookies:
                logger.info(cookie)

        # Обработка тела запроса
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            logger.info("Тело запроса: %s", post_data.decode('utf-8'))
        except (ValueError, json.JSONDecodeError) as e:
            logger.error("Ошибка обработки данных: %s", e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON format")
            return
        
        # Ответ на запрос
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"Result": True}).encode('utf-8'))

if __name__ == "__main__":
    server_address = ("192.168.1.7", 57070)
    httpd = HTTPServer(server_address, DahuaANPRHandler)
    logger.info(f"Сервер запущен на {server_address[0]}:{server_address[1]}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Остановка сервера.")
        httpd.server_close()