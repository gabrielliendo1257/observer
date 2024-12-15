import string, base64, re, socket
import netifaces as ni
from random import choice
from Cryptodome.Cipher import AES
from uuid import UUID
from ipaddress import ip_address


""" Colors """
MAIN = "\001\033[38;5;85m\002"
GREEN = "\001\033[38;5;82m\002"
GRAY = PLOAD = "\001\033[38;5;246m\002"
NAME = "\001\033[38;5;228m\002"
RED = "\001\033[1;31m\002"
FAIL = "\001\033[1;91m\002"
ORANGE = "\001\033[0;38;5;214m\002"
LRED = "\001\033[0;38;5;196m\002"
BOLD = "\001\033[1m\002"
PURPLE = "\001\033[0;38;5;141m\002"
BLUE = "\001\033[0;38;5;12m\002"
UNDERLINE = "\001\033[4m\002"
UNSTABLE = "\001\033[5m\002"
END = "\001\033[0m\002"


""" MSG Prefixes """
INFO = f"{MAIN}Info{END}"
WARN = f"{ORANGE}Warning{END}"
IMPORTANT = f"{ORANGE}Important{END}"
FAILED = f"{RED}Fail{END}"
ERR = f"{LRED}Error{END}"
DEBUG = f"{ORANGE}Debug{END}"
CHAT = f"{BLUE}Chat{END}"
GRN_BUL = f"[{GREEN}*{END}]"
ATT = f"{ORANGE}[!]{END}"


def get_random_str(length):
    # choose from all lowercase letter
    chars = string.ascii_lowercase + string.digits
    rand_str = "".join(choice(chars) for _ in range(length))
    return rand_str


def get_file_contents(path, mode="rb"):

    try:
        f = open(path, mode)
        contents = f.read()
        f.close()
        return contents

    except:
        return None


def is_valid_uuid(value):

    try:
        UUID(str(value))
        return True

    except:
        return False


def is_valid_ip(ip_addr):

    try:
        ip_address(ip_addr)
        return True

    except ValueError:
        return False


def parse_lhost(lhost_value):

    try:
        # Check if valid IP address
        lhost = str(ip_address(lhost_value))

    except ValueError:

        try:
            # Check if valid interface
            lhost = ni.ifaddresses(lhost_value)[ni.AF_INET][0]["addr"]

        except:
            return False

    return lhost


def get_datetime():
    from datetime import datetime

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date


def print_table(rows, columns):

    columns_list = [columns]

    for item in rows:

        # Values length adjustment
        try:
            for key in item.keys():
                item_to_str = str(item[key])
                item[key] = (
                    item[key]
                    if len(item_to_str) <= 20
                    else f"{item_to_str[0:8]}..{item_to_str[-8:]}"
                )

        except:
            pass

        columns_list.append(
            [str(item[col] if item[col] is not None else "") for col in columns]
        )

    col_size = [max(map(len, col)) for col in zip(*columns_list)]
    format_str = "  ".join(["{{:<{}}}".format(i) for i in col_size])
    columns_list.insert(1, ["-" * i for i in col_size])

    for item in columns_list:

        # Session Status ANSI
        item[-1] = f"{GREEN}{item[-1]}{END}" if item[-1] == "Active" else item[-1]
        item[-1] = (
            f"{ORANGE}{item[-1]}{END}"
            if (item[-1] in ["Unreachable", "Undefined"])
            else item[-1]
        )
        item[-1] = f"{LRED}{item[-1]}{END}" if (item[-1] in ["Lost"]) else item[-1]

        # Stability ANSI
        item[-2] = (
            f"{UNSTABLE}{item[-2]} {END}"
            if (columns_list[0][-2] == "Stability" and item[-2] == "Unstable")
            else item[-2]
        )
        print(format_str.format(*item))


def validate_host_address(addr):

    addr_verified = False
    try:
        # Check if valid IP address
        # re.search('[\d]{1,3}[\.][\d]{1,3}[\.][\d]{1,3}[\.][\d]{1,3}', lhost_value)
        addr_verified = str(ip_address(addr))

    except ValueError:

        try:
            # Check if valid interface
            addr_verified = ni.ifaddresses(addr)[ni.AF_INET][0]["addr"]

        except:
            # Check if valid hostname
            if len(addr) > 255:
                addr_verified = False
                print("Hostname length greater than 255 characters.")
                return False

            if addr[-1] == ".":
                addr = addr[
                    :-1
                ]  # Strip trailing dot (used to indicate an absolute domain name and technically valid according to DNS standards)

            disallowed = re.compile(r"[^A-Z\d-]", re.IGNORECASE)
            if all(
                len(part)
                and not part.startswith("-")
                and not part.endswith("-")
                and not disallowed.search(part)
                for part in addr.split(".")
            ):
                # Check if hostname is resolvable
                try:
                    socket.gethostbyname(addr)
                    addr_verified = addr

                except:
                    print("Failed to resolve LHOST.")

    return addr_verified


def encrypt_msg(aes_key, msg, iv):
    enc_s = AES.new(aes_key, AES.MODE_CFB, iv)

    if type(msg) == bytes:
        cipher_text = enc_s.encrypt(msg)
    else:
        cipher_text = enc_s.encrypt(msg.encode("utf-8"))

    encoded_cipher_text = base64.b64encode(cipher_text)
    return encoded_cipher_text


def decrypt_msg(aes_key, cipher, iv):

    try:
        decryption_suite = AES.new(aes_key, AES.MODE_CFB, iv)
        plain_text = decryption_suite.decrypt(base64.b64decode(cipher + b"=="))
        return (
            plain_text
            if type(plain_text) == str
            else plain_text.decode("utf-8", "ignore")
        )

    except TypeError:
        pass
