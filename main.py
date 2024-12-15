import socketserver
import threading
from observer.socks.configurations import TCP_Sock_Handler_Settings
from observer.socks.socket_server import ThreadedTcpRequestHandler, ReceiveMessage


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_port = True
    allow_reuse_address = True


def main():
    host = str(TCP_Sock_Handler_Settings.hostname(is_public=True))
    port = int(TCP_Sock_Handler_Settings.listener())
    print(host)

    while True:
        with ThreadedTCPServer((host, port), ThreadedTcpRequestHandler) as server:
            ThreadedTcpRequestHandler.decision(ReceiveMessage()).set_request(
                server.get_request()
            )
            print("Servidor conectado a: ", server.get_request()[1])
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()


if __name__ == "__main__":
    main()
