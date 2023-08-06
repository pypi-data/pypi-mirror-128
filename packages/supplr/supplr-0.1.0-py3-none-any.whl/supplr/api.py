from contextlib import contextmanager
from ctypes import *
import sys
import time
import datetime
import subprocess
import csv
import pandas as pd
import os

from multiprocessing.pool import ThreadPool
from supplr.struct import Data
from supplr.config import *
from supplr.struct import Frame
from supplr.struct import mapping
from supplr.struct import FrameBuf
from supplr.parser import parse_frame_voltage
from supplr.parser import parse_frame_temperature
from supplr.parser import parse_frame_reference_hv_voltage
from supplr.parser import parse
from supplr.board_id import get_board_id

chailib = CDLL("libchai.so")
chailib.CiInit.restype = c_int16
chailib.CiOpen.argtypes = [c_uint8, c_uint8]
chailib.CiOpen.restype = c_int16
chailib.CiStart.restype = c_int16
chailib.CiStart.argtypes = [c_uint8]
chailib.CiSetBaud.restype = c_int16
chailib.CiSetBaud.argtypes = [c_uint8, c_uint8, c_uint8]
chailib.CiStop.restype = c_int16
chailib.CiStop.argtypes = [c_uint8]
chailib.CiClose.restype = c_int16
chailib.CiClose.argtypes = [c_uint8]
chailib.CiWrite.argtypes = [c_uint8, POINTER(Frame), c_int16]
chailib.CiWrite.restype = c_int16
chailib.msg_zero.argtypes = [POINTER(Frame)]
chailib.CiRead.argtypes = [c_uint8, POINTER(FrameBuf), c_int16]
chailib.CiRead.restype = c_int16


@contextmanager
def can_init(board):
    try:
        can_open(board)
        yield
    finally:
        can_close(board)


def can_open(board):
    try:
        res_init_chai = init_chai()
        res_open_bus = open_bus(board)
        res_set_baud = set_baud(board)
        res_start_bus = start_bus(board)
        if -1 in (res_init_chai, res_open_bus, res_set_baud, res_start_bus):
            return -1
        else:
            return 0
    except:
        return -1


def can_close(board):
    try:
        res_stop_bus = stop_bus(board)
        res_close_bus = close_bus(board)
        if -1 in (res_stop_bus, res_close_bus):
            return -1
        else:
            return 0
    except:
        return -1


def init_chai():
    ret = chailib.CiInit()
    if ret < 0:
        return -1
    return 0


def open_bus(board):
    ret = chailib.CiOpen(get_board_id(board)["canch"], 2)
    if ret < 0:
        return -1
    return 0


def start_bus(board):
    ret = chailib.CiStart(get_board_id(board)["canch"])
    if ret < 0:
        return -1
    return 0

def set_baud(board):
    ret = chailib.CiSetBaud(get_board_id(board)["canch"], 0x0, 0x14)
    if ret < 0:
        return -1
    return 0


def close_bus(board):
    ret = chailib.CiClose(get_board_id(board)["canch"])
    if ret < 0:
        return -1
    return 0


def stop_bus(board):
    ret = chailib.CiStop(get_board_id(board)["canch"])
    if ret < 0:
        return -1
    return 0


def set_one_channel(board, mez, mezch, voltage):
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.set_one_channel(get_board_id(board)["write_id"], mez, mezch, voltage)
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -2
    return 0


def set_all_channels(board, voltage):
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.set_all_channels(get_board_id(board)["write_id"], voltage)
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -2
    return 0


def flud_off(board):
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.flud_off(get_board_id(board)["write_id"])
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -3
    return 0


def flud_on(board):
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.flud_on(get_board_id(board)["write_id"])
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -3
    return 0


def board_reset(board):
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.board_reset(get_board_id(board)["write_id"])
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -4
    return 0


def read_all_channel(board):
    for mez in range(4):
        for mezch in range(32):
            bit = read_one_channel(board, mez, mezch)
            while bit in (None, -5):
                bit = read_one_channel(board, mez, mezch)
            print("%4d %5d %8d" % (mez, mezch, bit))
    return 0


def read_mez_temperature(board, mez):
    def read_triada():
        framebuf = FrameBuf()
        pframebuf = pointer(framebuf)
        time.sleep(0.1)
        ret = chailib.CiRead(get_board_id(board)["canch"], pframebuf, 1)
        if ret < 0:
            pass
        else:
            data = parse_frame_temperature(pframebuf.contents[0])
            if get_board_id(board)["read_id"] == data["id"] and data["read_type"] == 5 and data["mez"] == mez:
                return data["temp"]
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(read_triada)
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.read_temperature_from_mez(get_board_id(board)["write_id"], mez)
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -6
    return async_result.get()


def read_one_channel(board, mez, mezch):
    def read_triada():
        framebuf = FrameBuf()
        pframebuf = pointer(framebuf)
        time.sleep(0.2)
        ret = chailib.CiRead(get_board_id(board)["canch"], pframebuf, 1)
        if ret < 0:
            pass
        else:
            data = parse_frame_voltage(pframebuf.contents[0])
            if get_board_id(board)["read_id"] == data["id"] and data["read_type"] == 4 and data["mez"] == mez and data["mezch"] == mezch:
                return data["voltage"]
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(read_triada)
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.read_one_channel(get_board_id(board)["write_id"], mez, mezch)
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -5
    return async_result.get()


def read_reference_voltage(board):
    def read_triada():
        framebuf = FrameBuf()
        pframebuf = pointer(framebuf)
        time.sleep(0.1)
        ret = chailib.CiRead(get_board_id(board)["canch"], pframebuf, 1)
        if ret < 0:
            pass
        else:
            data = parse_frame_reference_hv_voltage(pframebuf.contents[0])
            if get_board_id(board)["read_id"] == data["id"] and data["read_type"] == 2:
                return data["voltage"]
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(read_triada)
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.read_reference_voltage(get_board_id(board)["write_id"])
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -7
    return async_result.get()


def read_hv_supply_voltage(board):
    def read_triada():
        framebuf = FrameBuf()
        pframebuf = pointer(framebuf)
        time.sleep(0.1)
        ret = chailib.CiRead(get_board_id(board)["canch"], pframebuf, 1)
        if ret < 0:
            pass
        else:
            data = parse_frame_reference_hv_voltage(pframebuf.contents[0])
            if get_board_id(board)["read_id"] == data["id"] and data["read_type"] == 2:     #Должен возвращать кадр с индификатором 0х12. Возвращает 0х02
                return data["voltage"]
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(read_triada)
    frame = Frame()
    chailib.msg_zero(pointer(frame))
    frame.read_hv_supply_voltage(get_board_id(board)["write_id"])
    ret = chailib.CiWrite(get_board_id(board)["canch"], pointer(frame), 1)
    if ret < 0:
        return -8
    return async_result.get()


#Volt ---> bit
def find_volt_to_bit(board, mez, mezch, voltage):
    DAC_RES = 2**14
    file_name = CAL_DIR + "/board_" + str(board) + "_ref2.500" + "/board_"+str(board)+"_mez_"+str(mez)+"_mezch_"+str(mezch)+"_reconstruct_16384.txt"
    df = pd.read_csv(file_name, skiprows = 6,header = None)
    step = df[2][DAC_RES - 1]/DAC_RES
    bit_list = df[(df[2] >= voltage-step) & (df[2] <= voltage+step)][0].values
    diff_volt = [abs(voltage - df[2][i]) for i in bit_list]
    bit = bit_list[diff_volt.index(min(diff_volt))]
    return bit


#ADC code ---> volts from mez calibration file
def find_ADC_to_volt(board, mez, ADC_code):
    DAC_RES = 2**14
    file_name = CAL_DIR + "/board_" + str(board) + "_ref2.500" + "/board_"+str(board)+"_mez_"+str(mez)+"_mezch_0_points_16384.txt"
    df = pd.read_csv(file_name, skiprows = 6,header = None)
    step = df[1][len(df[1]) - 1]/len(df[1])
    ADC_list = df[(df[1] >= ADC_code-step) & (df[1] <= ADC_code+step)][1].values
    voltage_list = df[(df[1] >= ADC_code-step) & (df[1] <= ADC_code+step)][2].values
    diff_ADC = [abs(ADC_code - ADC) for ADC in ADC_list]
    index_ADC = diff_ADC.index(min(diff_ADC))
    return voltage_list[index_ADC]


#ADC code ---> volts from channel calibration file
def find_ADC_to_volt_channel(board, mez, mezch, ADC_code):
    DAC_RES = 2**14
    file_name = CAL_DIR + "/board_" + str(board) + "_ref2.500" + "/board_"+str(board)+"_mez_"+str(mez)+"_mezch_"+str(mezch)+"_reconstruct_16384.txt"
    df = pd.read_csv(file_name, skiprows = 6,header = None)
    step = df[1][len(df[1]) - 1]/len(df[1])
    ADC_list = df[(df[1] >= ADC_code-step) & (df[1] <= ADC_code+step)][1].values
    voltage_list = df[(df[1] >= ADC_code-step) & (df[1] <= ADC_code+step)][2].values
    diff_ADC = [abs(ADC_code - ADC) for ADC in ADC_list]
    if diff_ADC:
        index_ADC = diff_ADC.index(min(diff_ADC))
        return voltage_list[index_ADC]


#ADC code ---> bit
def find_ADC_to_bit(board, mez, mezch, ADC_code):
    DAC_RES = 2**14
    file_name = CAL_DIR + "/board_" + str(board) + "_ref2.500" + "/board_"+str(board)+"_mez_"+str(mez)+"_mezch_"+str(mezch)+"_reconstruct_16384.txt"
    df = pd.read_csv(file_name, skiprows = 6,header = None)
    step = df[1][DAC_RES - 1]/DAC_RES
    ADC_list = df[(df[1] >= ADC_code-step) & (df[1] <= ADC_code+step)][0].values
    diff_ADC = [abs(ADC_code - df[1][i]) for i in ADC_list]
    bit = ADC_list[diff_ADC.index(min(diff_ADC))]
    return bit


def set_voltage_volt(board, mez, mezch, voltage):
    try:
        bit = find_volt_to_bit(board, mez, mezch, voltage)
        set_one_channel(board, mez, mezch, int(hex(bit), 16))
    except:
        print("No calibration file!")
        return -10
    return 0


def set_voltage_all_volt(board, voltage):
    for mez in range(4):
        for mezch in range(32):
            channel = mez_mezch_converter(mez, mezch)
            for attempt in range(3):
                set_voltage_volt(board, mez, mezch, voltage)
                time.sleep(0.05)
            print("%2d %2d %3d %4d | voltage: %8.4f V" % (board, mez, mezch, channel, voltage))


def read_channel_volt(board, mez, mezch):
    try:
        ADC_code = read_one_channel(board, mez, mezch)
        while ADC_code is None:
            ADC_code = read_one_channel(board, mez, mezch)
        if ADC_code < 9000:
            voltage = 0.2
        else:
            voltage = find_ADC_to_volt_channel(board, mez, mezch, ADC_code)
            if voltage == None:
                return {"ADC_code": ADC_code, "voltage": 0.2}
        return {"ADC_code": ADC_code, "voltage": voltage}
    except:
        return -5


def read_all_channel_volt(board):
    for mez in range(4):
        for mezch in range(32):
            try:
                ADC_code = read_one_channel(board, mez, mezch)
                while ADC_code is None:
                    ADC_code = read_one_channel(board, mez, mezch)
                voltage = find_ADC_to_volt_channel(board, mez, mezch, ADC_code)
                channel = mez_mezch_converter(mez, mezch)
                if voltage == None:
                    voltage = 0.2
                    print("%2d %2d %3d %4d | ADC code: %8d  | voltage: %8.4f V" % (board, mez, mezch, channel, ADC_code, voltage))
                else:
                    print("%2d %2d %3d %4d | ADC code: %8d  | voltage: %8.4f V" % (board, mez, mezch, channel, ADC_code, voltage))
            except:
                    pass


def read_voltage_from_file_path(board, file_name):
    df = pd.read_csv(file_name, skiprows = 0,header = None)
    for row in df.itertuples(index=False):
        channel = row[0]
        mez_mezch = channel_converter(channel)
        time.sleep(0.1)    #Need check delay
        result = read_channel_volt(board, mez_mezch["mez"], mez_mezch["mezch"])
        print("%2d %2d %3d %4d |  voltage: %8.4f V" % (board, mez_mezch["mez"], mez_mezch["mezch"], channel, round(result["voltage"],4)))


#channel ---> mez, mezch
def channel_converter(channel):
    if 0<=channel<=31:
        mez = 0
        mezch = channel
    elif 32<=channel<=63:
        mez = 1
        mezch = channel - 32
    elif 64<=channel<=95:
        mez = 2
        mezch = channel - 64
    elif 96<=channel<=127:
        mez = 3
        mezch = channel - 96
    return {"mez": mez, "mezch": mezch}


#mez, mezch ---> channel
def mez_mezch_converter(mez, mezch):
    if mez == 0:
        channel = mezch
    elif mez == 1:
        channel = 32 + mezch
    elif mez == 2:
        channel = 64 + mezch
    elif mez == 3:
        channel = 96 + mezch
    return channel


def ref_manage(board):
    ref_value = read_reference_voltage(board)
    if 1.025<ref_value<1.5:
        ref = "_ref1.250"
    elif 1.9<ref_value<2.2:
        ref = "_ref2.048"
    elif 2.4<ref_value<2.6:
        ref = "_ref2.500"
    elif 3.9<ref_value<4.2:
        ref = "_ref4.096"
    else:
        print("Is there something wrong with jumper!!!")
        sys.exit()
    return ref


def set_voltage_from_file_path(board, file_name):
    df = pd.read_csv(file_name, skiprows = 0,header = None)
    for row in df.itertuples(index=False):
        channel = row[0]
        convert = channel_converter(channel)
        mez = convert["mez"]
        mezch = convert["mezch"]
        voltage = row[1]
        for attempt in range(6):
            set_voltage_volt(board, mez, mezch, voltage)
            time.sleep(0.03)
        print("%2d %2d %3d %4d |  voltage: %8.2f V" % (board, mez, mezch, channel, voltage))


CL = 0.01 #V
def correction_voltage(board, mez, mezch, voltage):
    voltage_from_board = read_channel_volt(board, mez, mezch)
    difference_voltage = voltage - voltage_from_board["voltage"]
    voltage_correction = voltage + difference_voltage
    while abs(difference_voltage) > CL:
        set_voltage_volt(board, mez, mezch, voltage_correction)
        voltage_from_board = read_channel_volt(board, mez, mezch)
        difference_voltage = voltage - voltage_from_board["voltage"]
        voltage_correction = voltage_correction + difference_voltage
    voltage_from_board = read_channel_volt(board, mez, mezch)
    print(f"board: {board}, mez: {mez}, mezch: {mezch}, voltage: {voltage_from_board}V")


def correction_voltage_from_file(board, file_name):
    df = pd.read_csv(file_name, skiprows = 0,header = None)
    for row in df.itertuples(index=False):
        convert = channel_converter(row[0])
        mez = convert["mez"]
        mezch = convert["mezch"]
        voltage = row[1]
        correction_voltage(board, mez, mezch, voltage)


def board_status():
    init_chai_res = init_chai()
    if init_chai_res < 0:
        print("CAN-bus-USB didn't connected!")
        return -1
    board_numbers = []
    for board in range(10): #number of boards
        try:
            ret = get_board_id(board)
            board_numbers.append(board)
        except:
            pass
    for board in board_numbers:
        open_bus(board)
        set_baud(board)
        start_bus(board)
        flud_off(board)
        time.sleep(0.1)
        board_reset(board)
        time.sleep(0.1)
        status = []
        for attempt in range(3):
            ret = read_one_channel(board, 0, 0)
            if ret in (None, -5):
                status.append(False)
            else:
                status.append(True)
        if True in status:
            print(f"Board #{board}: CONNECTED!")
        else:
            print(f"Board #{board}: NOT FOUND!")
        can_close(board)
    return 0


def calib_path():
    print(CAL_DIR)
