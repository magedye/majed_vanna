import socket
def find_available_port(start_port=8000, attempts=20):
    for i in range(attempts):
        port=start_port+i
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try: s.bind(("0.0.0.0",port)); return port
            except OSError: continue
    raise RuntimeError("No free ports")
