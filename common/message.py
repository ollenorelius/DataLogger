import struct
import json

def get_chksum(data):
    return bytes([0xFF])

class Message():
    DL = 2
    data = b''

    def __init__(self):
        """
        Parent class for messages routed. 

        conn is the socket used to construct this message.
        """

    def deserialize(self, data):
        self.data = json.loads(data[:-1].decode('utf8'))
        self.chk = data[-1]
        if 'name' not in self.data or 'data_type' not in self.data:
            self.name = ''
            self.data_type = ''
            print("Got invalid %s package, data: %s" % (type(self), self.data))
            return False

    def serialize(self):
        json_data = bytes(json.dumps(self.data), encoding="utf8")
        json_data += get_chksum(json_data)
        return self.get_key_bytes() + struct.pack(">L", len(json_data)) + json_data

    def create_from_local_data(self, data):
        pass

    def read_data(self, data):
        pass

    def create(self, *args, **kwargs):
        pass

    def get_key_bytes(self):
        byte = list(message_list.keys())[list(message_list.values()).index(type(self))]
        inv_byte = 0xFF ^ byte
        return bytes([byte, inv_byte])


class StartMeasurement(Message):
    def __init__(self):
        super().__init__()

    def deserialize(self, data):
        self.data = json.loads(data[:-1].decode('utf8'))
        self.chk = data[-1]
        if 'name' not in self.data or 'data_type' not in self.data:
            self.name = ''
            self.data_type = ''
            print("Got invalid StartMeasurement package, data: %s" % self.data)
            return False
    
    def serialize(self):
        json_data = bytes(json.dumps(self.data), encoding="utf8")
        json_data += get_chksum(json_data)
        return self.get_key_bytes() + struct.pack(">L", len(json_data)) + json_data

    def create(self, name, data_t):
        self.data = {"name":name, "data_type":data_t}


class ContinueMeasurement(Message):
    def __init__(self):
        super().__init__()

    def deserialize(self, data):
        data_json = json.loads(data[:-1].decode('utf8'))
        self.chk = data[-1]
        if 'name' not in data_json or 'data_type' not in data_json:
            self.name = ''
            self.data_type = ''
            return

        self.name = data_json['name']
        self.data_type = data_json['data_type']



message_list = {0x00: Message,
                0x01: StartMeasurement,
                0x02: ContinueMeasurement}
