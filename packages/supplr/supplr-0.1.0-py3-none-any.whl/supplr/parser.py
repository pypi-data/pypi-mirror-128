from supplr.struct import *

def parse(frame):
    print([i for i in frame.data])
    return {
        0x04: parse_voltage,
        0x05: parse_temperature,
    }[frame.data[0]](frame)


def parse_frame_voltage(frame):
    voltage = 0
    voltage = voltage|frame.data[3]
    voltage = (frame.data[4]<<8)|voltage
    voltage = (frame.data[5]<<16)|voltage
    voltage = (frame.data[6]<<24)|voltage  #Для получения значения в мВ нужно подельть на 1000. Сейчас напряжение в кодах АЦП (прошивка 17.08.21)
    id = frame.id
    read_type = frame.data[0]
    mez = frame.data[1]
    mezch = frame.data[2]
    # return [id, read_type, mez, mez_ch, voltage]
    return {"id": id, "read_type": read_type, "mez": mez, "mezch": mezch, "voltage": voltage}


def parse_frame_temperature(frame):
    temp = 0
    temp = temp|frame.data[3]
    temp = (frame.data[4]<<8)|temp
    temp = (frame.data[5]<<16)|temp
    temp = (frame.data[6]<<24)|temp
    temp = temp/1000
    id = frame.id
    read_type = frame.data[0]
    mez = frame.data[1]
    # return [id, read_type, mez, temp]
    return {"id": id, "read_type": read_type, "mez": mez, "temp": temp}


def parse_frame_reference_hv_voltage(frame):
    voltage = 0
    voltage = voltage|frame.data[3]
    voltage = (frame.data[4]<<8)|voltage
    voltage = (frame.data[5]<<16)|voltage
    voltage = (frame.data[6]<<24)|voltage
    voltage = voltage/1000
    id = frame.id
    read_type = frame.data[0]
    # return [id, read_type, voltage]
    return {"id": id, "read_type": read_type, "voltage": voltage}
