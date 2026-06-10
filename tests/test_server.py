import http.server
import socketserver
import json
import sys
import os

# Puerto por defecto
PORT = 8000
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

# Resolver la raíz del proyecto para servir archivos locales
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Intercepta las solicitudes POST en /api/results para recibir reportes de prueba."""
        if self.path == '/api/results':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            results = json.loads(post_data.decode('utf-8'))
            
            # Guardar el JSON del reporte en tests/results.json
            results_path = os.path.join(project_root, 'tests', 'results.json')
            os.makedirs(os.path.dirname(results_path), exist_ok=True)
            
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            
            # Responder al cliente
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404, "Endpoint no encontrado")

    def log_message(self, format, *args):
        """Sobrescribe para mantener limpia la consola durante la ejecución automatizada."""
        pass

def run():
    # Evitar bloqueos de puerto en reinicios rápidos
    socketserver.TCPServer.allow_reuse_address = True
    
    # SimpleHTTPRequestHandler con el parámetro `directory` requiere Python 3.7+
    handler = lambda *args, **kwargs: TestServerHandler(*args, directory=project_root, **kwargs)
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Test server running on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDeteniendo servidor de pruebas...")

if __name__ == '__main__':
    run()
