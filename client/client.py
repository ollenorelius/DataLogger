import socket
import sys

sys.path.append(".")
import common.message as message

client_socket = socket.socket()
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(("localhost", 8000))

msg = message.StartMeasurement()
msg.create(name="Doop doop", data_t="Numeric")

client_socket.send(msg.serialize())
