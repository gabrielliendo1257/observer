from uuid import uuid4
import netifaces


class TCP_Sock_Handler_Settings:

    __interfaz = netifaces.gateways()["default"][netifaces.AF_INET][1]

    bind_address = None or netifaces.gateways()["default"][netifaces.AF_INET][0]
    bind_port = 4443
    sentinel_value = uuid4().hex
    sock_timeout = 4
    recv_timeout = 14
    recv_timeout_buffer_size = 4096
    await_execution_timeout = 90
    alive_echo_exec_timeout = 2.5

    # Max failed echo response requests before a connection is characterized as lost
    fail_count = 3

    # Check if connection is random socket connection by assessing the hostname value received.
    # This filter automatically rejects TCP reverse connection if they fail to pass validation tests.
    hostname_filter = True
    hostname_filter_warning_delivered = False

    port: int = 8080

    @classmethod
    def hostname(cls, is_public: bool = False):
        if is_public:
            print("Servidor en LAN.")
            return netifaces.ifaddresses(cls.__interfaz)[netifaces.AF_INET][0]["addr"]
        else:
            print("Servidor en localhost.")
            return "0.0.0.0"

    @classmethod
    def listener(cls, port: int = 8080):
        cls.port = port
        return cls.port
