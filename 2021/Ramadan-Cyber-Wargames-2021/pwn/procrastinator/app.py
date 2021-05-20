import socketserver
import subprocess

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Log connections
        print("{} connected.".format(self.client_address[0]))
        self.request.sendall(b'Welcome to the Procrastinator!\nJust enter how many seconds you would like to procrastinate for and we will keep you distracted!\nHow many seconds would like to procrastinate? ')
        self.seconds = self.request.recv(1024).decode().strip()
        try:
            self.seconds = int(self.seconds)
            if self.seconds > 10:
                self.request.sendall(b'\nSorry! You can procrasinate for a maximum of 10 seconds.\n')
        except ValueError:
            pass

            # Execute the command
            self.request.sendall(f'\nProcrastinating for "{self.seconds}" seconds...\n'.encode('utf-8'))
            try:
                self.output = subprocess.check_output(f'sleep {self.seconds.replace(";", "").replace("&", "").replace("{", "").replace("}", "")} && echo "Wake up!"', shell=True)
                if len(self.output) > 0:
                    self.request.sendall(f'\n{self.output.decode("utf-8")}\n'.encode('utf-8'))
                self.request.sendall(b'Done procrastinating! Hope you enjoyed, bye!\n')
            except Exception as e:
                self.request.sendall(f'\nOops! There was an error procrastinating! Here it is: {str(e)}\n'.encode('utf-8'))
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9812
    socketserver.ForkingTCPServer.allow_reuse_address = True
    with socketserver.ForkingTCPServer((HOST, PORT), TCPHandler) as server:
        try :
            print("Server started on port 9812")
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
        except Exception:
            pass
