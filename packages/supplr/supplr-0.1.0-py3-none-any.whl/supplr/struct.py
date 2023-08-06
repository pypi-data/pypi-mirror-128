from ctypes import Array
from ctypes import Structure
from ctypes import c_uint32
from ctypes import c_uint8
from ctypes import c_uint16


class Data(Array):
    _type_ = c_uint8
    _length_ = 8

class Frame(Structure):
    _fields_ = [
        ("id", c_uint32),
        ("data", Data),
        ("len", c_uint8),
        ("flags", c_uint16),
        ("ts", c_uint32),
    ]

    def set_one_channel(self, board, mez, mezch, voltage):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x10
        self.data[1] = mez & 0xff
        self.data[2] = mapping[mezch]
        self.data[3] = voltage & 0xff
        self.data[4] = (voltage >> 8) & 0xff
        self.data[5] = 0x00
        self.data[6] = 0x00


    def set_all_channels(self, board, voltage):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x11
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = voltage & 0xff
        self.data[4] = (voltage >> 8) & 0xff
        self.data[5] = 0x00
        self.data[6] = 0x00


    def flud_off(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x03
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def mode_code(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x20
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def mode_voltage(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x20
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x01
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00


    def flud_on(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x03
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x01
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def board_reset(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x01
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def read_one_channel(self, board, mez, mezch):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x04
        self.data[1] = mez & 0xff
        self.data[2] = mezch & 0xff
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def read_reference_voltage(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x02
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def read_hv_supply_voltage(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x12
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def read_temperature_from_mez(self, board, mez):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x05
        self.data[1] = mez & 0xff
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

    def read_all_channel(self, board):
        self.id = board
        self.flags = 0
        self.len = 7
        self.data[0] = 0x04
        self.data[1] = 0x00
        self.data[2] = 0x00
        self.data[3] = 0x00
        self.data[4] = 0x00
        self.data[5] = 0x00
        self.data[6] = 0x00

class FrameBuf(Array):
    _length_ = 1
    _type_ = Frame

mapping = [
    10,6,8,5,2,3,0,1,
    4,12,7,9,14,11,13,15,
    16,17,18,20,19,21,25,22,
    26,29,23,24,31,30,28,27,
]

__all__ = ["Data", "Frame", "mapping", "FrameBuf"]
