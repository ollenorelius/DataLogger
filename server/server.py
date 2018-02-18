import socket
import threading
import time
import sys
import struct

sys.path.append(".")
import common.message as message

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

def handler_thread(client):
    last_byte = b''
    in_byte = b''
    while(1):
        time.sleep(0.01)
        last_byte = in_byte
        in_byte = client.recv(1)
        if in_byte != b'':
            print(in_byte)
        if last_byte != b'' and int.from_bytes(in_byte, "little") == int.from_bytes(last_byte, "little") ^ 0xFF:
            DL_raw = conn.recv(4)
            DL = struct.unpack(">L", DL_raw)[0]
            data = conn.recv(DL)
            message_type = int.from_bytes(last_byte, "little")
            msg = message.message_list[message_type]()
            print(data)
            msg.deserialize(data)
            print(msg.data['name'])

if __name__ == "__main__":
    print("Server started! Awaiting connections.")
    while(True):
        conn, add = server_socket.accept()
        threading.Thread(target=handler_thread,
                         args=[conn],
                         daemon=True).start()
        print(conn)
