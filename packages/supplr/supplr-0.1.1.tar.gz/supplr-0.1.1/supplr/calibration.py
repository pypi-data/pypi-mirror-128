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
from supplr.api import *

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


def start_calib_measurement(board, kport):
    command = 'sudo chown root:adm /dev/ttyUSB'+str(kport)
    subprocess.check_output(command,shell=True)
    command_root = 'find /dev/bus/usb -type c | sudo xargs chown root:adm'
    subprocess.check_output(command_root,shell=True)
    ttycmd = 'echo ":SYST:BEEP:STAT OFF">>/dev/ttyUSB'+str(kport)
    subprocess.check_output(ttycmd,shell=True)
    init_chai()
    open_bus(board)
    set_baud(board)
    start_bus(board)
    for attempt in range(6):
        board_reset(board)
        time.sleep(0.03)
    for attempt in range(6):
        flud_off(board)
        time.sleep(0.03)


def finish_calib_measurement(board, kport):
    stop_bus(board)
    close_bus(board)
    ttycmd = 'echo ":SYST:PRES">>/dev/ttyUSB'+str(kport)
    subprocess.check_output(ttycmd,shell=True)
    ttycmd = 'echo ":SYST:LOC">>/dev/ttyUSB'+str(kport)
    subprocess.check_output(ttycmd,shell=True)


def reference_voltage(board):
    for attempt in range(6):
        ref_value = read_reference_voltage(board)
        if ref_value is not None:
            break
    return ref_value


def voltage_setting(board, mez, mezch, voltage):
    for attempt in range(6):
        set_one_channel(board, mez, mezch, voltage)
        time.sleep(0.03)

def voltage_ADC(board, mez, mezch):
    try:
        for attempt in range(6):
            voltage_from_board = read_one_channel(board, mez, mezch)
            if voltage_from_board is not None:
                break
    except:
        voltage_from_board = 0
    if voltage_from_board is None:
        voltage_from_board = 0
    return voltage_from_board


def mez_temperature(board, mez):
    try:
        for attempt in range(6):
            temperature_from_board = read_mez_temperature(board, mez)
            if temperature_from_board is not None:
                break
    except:
        temperature_from_board = 0
    if temperature_from_board is None:
        temperature_from_board = 0
    return temperature_from_board


def calibration(board, mez, mezch, kport, points):
    start_calib_measurement(board, kport)
    answer = input("Continue scanning(c) or scan from scratch(s): ")
    while answer not in ("c", "s"):
        answer = input("Continue scanning(c) or scan from scratch(s): ")
    if answer == "s":
        bit_continue = 0
        text_add = ""
    else:
        bit_continue = int(input("Enter start point (0-16384): "))
        text_add = "_add" + str(bit_continue)
    ref_value = reference_voltage(board)
    print("Ref.value: " + str(ref_value))
    if 1.025<ref_value<1.5:
        ref = "_ref1.250"
    elif 1.9<ref_value<2.2:
        ref = "_ref2.048"
    elif 2.4<ref_value<2.6:
        ref = "_ref2.500"
    elif 3.9<ref_value<4.2:
        ref = "_ref4.096"
    else:
        print("Is there something wrong!!!")
        print("Bye-Bye!")
        sys.exit()
    board_dir = CAL_DIR_RAW + "/board_" + str(board) + str(ref)
    if not os.path.exists(board_dir):
        os.makedirs(board_dir)
    file_name = board_dir + "/board_"+str(board)+"_mez_"+str(mez)+"_mezch_"+str(mezch)+"_points_"+str(points)+text_add+"*TEST*.txt"
    print(file_name)
    csv_file = open(file_name, mode='w')
    writer = csv.writer(csv_file)
    start = datetime.datetime.today().replace(microsecond=0)
    writer.writerow(["Timestamp: " + str(start)])
    writer.writerow(["Board.id: " + str(board)])
    writer.writerow(["Ref.value: " + str(ref_value)])
    writer.writerow(["DAC,bit", "ADC,code", "K2000,V", "Tchip,C"])
    step = int(16384/points)
    voltage_bit_values = [i-1 for i in range(1,16385) if i%step == 0]
    voltage_bit_values.insert(0,0)
    for voltage_bit_value in voltage_bit_values:
        if voltage_bit_value<bit_continue:
            continue
        time.sleep(0.03) #???
        voltage = int(hex(voltage_bit_value), 16)
        voltage_setting(board, mez, mezch, voltage)
        voltage_from_board = voltage_ADC(board, mez, mezch)
        temperature_from_board = mez_temperature(board, mez)
        ttycmd = 'echo ":MEAS?">>/dev/ttyUSB'+str(kport)+' && head -n1 /dev/ttyUSB'+str(kport)
        voltage_from_k2000 = float(subprocess.check_output(ttycmd,shell=True))
        if voltage_bit_value>127 and voltage_from_k2000 < 0.5:
            print("BAD POINT!!!")
            voltage_setting(board, mez, mezch, voltage)
            voltage_from_board = voltage_ADC(board, mez, mezch)
            temperature_from_board = mez_temperature(board, mez)
            ttycmd = 'echo ":MEAS?">>/dev/ttyUSB'+str(kport)+' && head -n1 /dev/ttyUSB'+str(kport)
            voltage_from_k2000 = float(subprocess.check_output(ttycmd,shell=True))
        writer.writerow([voltage_bit_value, voltage_from_board, voltage_from_k2000, temperature_from_board])
        cur_time = datetime.datetime.today().replace(microsecond=0)
        print("%2d %2d %3d | %7s %8d %8d %12d %12.4f %12.4f" % (board, mez, mezch, cur_time, int(voltage_bit_value/step), voltage_bit_value, voltage_from_board, voltage_from_k2000, temperature_from_board))
    csv_file.close()
    finish_calib_measurement(board, kport)
    finish = datetime.datetime.today().replace(microsecond=0)
    print(f"Start time: {start}")
    print(f"Finish time: {finish}")
    print(f"Calibration time: {finish - start}")


def calibration_one_measurement(board, mez, mezch, kport, voltage):
    start_calib_measurement(board, kport)
    voltage_bit = int(hex(voltage), 16)
    measurements = []
    ref_value = reference_voltage(board)
    print("Ref.value: " + str(ref_value))
    for attempt in range(2):
        voltage_setting(board, mez, mezch, voltage_bit)
        voltage_from_board = voltage_ADC(board, mez, mezch)
        temperature_from_board = mez_temperature(board, mez)
        ttycmd = 'echo ":MEAS?">>/dev/ttyUSB'+str(kport)+' && head -n1 /dev/ttyUSB'+str(kport)
        voltage_from_k2000 = float(subprocess.check_output(ttycmd,shell=True))
        print(board, mez, mezch, "|", attempt, voltage_from_board, voltage_from_k2000, temperature_from_board)
        measurements.append((voltage, voltage_from_board, voltage_from_k2000, temperature_from_board))
    finish_calib_measurement(board, kport)
    print("*************************************")
    for measurement in measurements:
        print(*measurement, sep=",")
