import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# ПРАВИЛЬНЫЙ путь без лишних пробелов
BASE_DIR = "/home/andrej/Poetry_homework/web_development-frontend-with-bootstrap/html"


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path.split("?")[0]
            if path == "/":
                path = "/index.html"

            full_path = os.path.normpath(os.path.join(BASE_DIR, path.lstrip("/")))

            if not os.path.exists(full_path):
                self.send_error(404, f"File not found: {path}")
                return

            with open(full_path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())

        except Exception as e:
            try:
                self.send_error(500, f"Error: {str(e)}")
            except BrokenPipeError:
                pass


if __name__ == "__main__":
    # Проверка перед запуском
    print("=" * 50)
    print(f"Проверка пути: {BASE_DIR}")
    print("Существует:", os.path.exists(BASE_DIR))
    if os.path.exists(BASE_DIR):
        print("Содержимое:", os.listdir(BASE_DIR))
    print("=" * 50)

    if not os.path.exists(BASE_DIR):
        print(f"ОШИБКА: Папка {BASE_DIR} не существует!")
        print("1. Проверьте путь на лишние пробелы")
        print("2. Создайте папку: mkdir -p " + BASE_DIR)
        exit(1)

    server = HTTPServer(("localhost", 8080), MyServer)
    print("Сервер запущен: http://localhost:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Сервер остановлен")
