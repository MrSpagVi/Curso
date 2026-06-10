import subprocess
import sys
import os
import time
import json
import socket

def find_free_port():
    """Selecciona dinámicamente un puerto de red libre."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def locate_browser():
    """
    Busca ejecutables de Microsoft Edge o Mozilla Firefox 
    en rutas típicas de Windows para ejecución headless.
    """
    edge_paths = [
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'Microsoft\\Edge\\Application\\msedge.exe'),
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Microsoft\\Edge\\Application\\msedge.exe'),
        os.path.join(os.environ.get('LocalAppData', 'C:\\Users\\default\\AppData\\Local'), 'Microsoft\\Edge\\Application\\msedge.exe'),
    ]
    
    firefox_paths = [
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'Mozilla Firefox\\firefox.exe'),
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'Mozilla Firefox\\firefox.exe'),
    ]

    for path in edge_paths:
        if os.path.exists(path):
            return path, 'edge'
            
    for path in firefox_paths:
        if os.path.exists(path):
            return path, 'firefox'
            
    return None, None

def run():
    print("Iniciando infraestructura de pruebas de estrés E2E...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_file = os.path.join(project_root, 'tests', 'results.json')
    
    # 1. Limpieza de resultados anteriores
    if os.path.exists(results_file):
        try:
            os.remove(results_file)
        except OSError as e:
            print(f"Advertencia: no se pudo eliminar el archivo residual: {e}")
        
    # 2. Selección de puerto e inicio del servidor local de pruebas
    port = find_free_port()
    server_script = os.path.join(project_root, 'tests', 'test_server.py')
    
    print(f"Lanzando servidor de pruebas en puerto {port}...")
    server_proc = subprocess.Popen(
        [sys.executable, server_script, str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_root
    )
    
    # Esperar a que el servidor esté listo
    server_ready = False
    for _ in range(50):
        try:
            with socket.create_connection(('localhost', port), timeout=0.1):
                server_ready = True
                break
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.1)
            
    if not server_ready:
        print("Error: El servidor local de pruebas no respondió a tiempo.")
        server_proc.terminate()
        sys.exit(1)
        
    # 3. Localizar navegador
    browser_path, browser_type = locate_browser()
    if not browser_path:
        print("Error crítico: No se encontró Edge ni Firefox.")
        server_proc.terminate()
        sys.exit(1)
        
    print(f"Navegador detectado: {browser_path} ({browser_type})")
    
    # 4. Lanzar el navegador headless apuntando a stress_runner.html
    url = f"http://localhost:{port}/tests/stress_runner.html"
    
    if browser_type == 'edge':
        args = [browser_path, '--headless=new', '--disable-gpu', '--no-sandbox', url]
    else:  # firefox
        args = [browser_path, '--headless', url]
        
    print(f"Ejecutando suite de estrés de forma headless...")
    browser_proc = subprocess.Popen(
        args, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    # 5. Esperar reporte de resultados
    timeout = 30  # segundos
    start_time = time.time()
    results = None
    
    try:
        while time.time() - start_time < timeout:
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r', encoding='utf-8') as f:
                        results = json.load(f)
                    break
                except json.JSONDecodeError:
                    time.sleep(0.1)
                    continue
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nEjecución cancelada.")
    finally:
        print("Finalizando procesos...")
        browser_proc.terminate()
        try:
            browser_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            browser_proc.kill()
            
        server_proc.terminate()
        try:
            server_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_proc.kill()
            
    if not results:
        print("Error: Tiempo de espera agotado sin recibir reporte.")
        sys.exit(1)
        
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("             RESULTADOS DE LAS PRUEBAS DE ESTRÉS")
    print("=" * 60)
    
    summary = results['summary']
    print(f"Resumen: {summary['passed']}/{summary['total']} exitosos | {summary['failed']} fallidos | {summary['duration_ms']}ms\n")
    
    failures_detected = False
    for t in results['tests']:
        status_char = "PASS" if t['status'] == 'passed' else "FAIL"
        print(f"[{status_char}] {t['name']} ({t['duration_ms']}ms)")
        if t['status'] != 'passed':
            failures_detected = True
            print(f"    Detalle: {t.get('error', 'Sin especificar')}")
            
    print("=" * 60)
    
    if os.path.exists(results_file):
        try:
            os.remove(results_file)
        except OSError:
            pass
            
    if failures_detected:
        print("Suite de estrés: SE ENCONTRARON VULNERABILIDADES O ERRORES.")
        sys.exit(1)
    else:
        print("Suite de estrés: ¡TODAS LAS PRUEBAS DE ESTRÉS PASARON CON ÉXITO!")
        sys.exit(0)

if __name__ == '__main__':
    run()
