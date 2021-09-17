import socketserver

print("Booting up server...")

class MYTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        received_data = self.request.recv(1024).strip()
        data = received_data.decode()
        print("data logs: " + data)
        
        
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    
    server = socketserver.ThreadingTCPServer((host, port), MYTCPHandler)
    server.serve_forever()
