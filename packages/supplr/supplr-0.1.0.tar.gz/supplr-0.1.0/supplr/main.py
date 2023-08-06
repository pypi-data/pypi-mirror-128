import click
from contextlib import contextmanager
import subprocess
from time import sleep

from supplr import api
import supplr.calibration as calib


@click.group()
def cli():
    """
    Application for working with power boards \"Marathon firm\"
    """


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
@click.option("--voltage", required=True, help="Voltage value in bits (0-16383)")
def set_channel_bit(board, mez, mezch, voltage):
    """*Set channel voltage by bits"""
    with api.can_init(board):
        api.set_one_channel(board, mez, mezch, int(voltage, 16))


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
@click.option("--voltage", required=True, type=float, help="Voltage value in volts")
def set_channel_volt(board, mez, mezch, voltage):
    """*Set channel voltage by volts"""
    with api.can_init(board):
        api.set_voltage_volt(board, mez, mezch, voltage)

@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--voltage", required=True, type=float, help="Voltage value in volts")
def set_channels_volt(board, voltage):
    """*Set voltage to all channels in volts"""
    with api.can_init(board):
        api.set_voltage_all_volt(board, voltage)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--voltage", required=True, help="Voltage value in bits (0-16383)")
def set_channels_bit(board, voltage):
    """*Set voltage to all channels in bits"""
    with api.can_init(board):
        api.set_all_channels(board, int(voltage, 16))


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def reset(board):
    """*Board reset"""
    with api.can_init(board):
        api.board_reset(board)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def flud_off(board):
    """*Board frame sending is disabled"""
    with api.can_init(board):
        api.flud_off(board)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def flud_on(board):
    """*Board frame sending is enabled"""
    with api.can_init(board):
        api.flud_on(board)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
def mez_temperature(board, mez):
    """*Get temperature from ADC chip"""
    with api.can_init(board):
        result = api.read_mez_temperature(board, mez)
        print(f"Temperature (C): {result}")


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def read_channels_bit(board):
    """*Get channel voltages in ADC code"""
    with api.can_init(board):
        api.read_all_channel(board)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
def read_channel_bit(board, mez, mezch):
    """*Get channel voltage in ADC code"""
    with api.can_init(board):
        result = api.read_one_channel(board, mez, mezch)
        print(f"Voltage: {result}")


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def read_reference_voltage(board):
    """*Get reference voltage"""
    with api.can_init(board):
        result = api.read_reference_voltage(board)
        print(f"Reference voltage (V): {result}")


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def read_hv_supply_voltage(board):
    """*Get high voltage power supply"""
    with api.can_init(board):
        result = api.read_hv_supply_voltage(board)
        print(f"Supply voltage (V): {result}")


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
@click.option("--kport", required=True, type=int, help="Multimeter USB port number (ttyUSB*)")
@click.option("--points", required=True, type=int, help="Number of scan points")
def calib(board, mez, mezch, kport, points):
    """*Calibration mode for a single channel"""
    calib.calibration(board, mez, mezch, kport, points)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
@click.option("--kport", required=True, type=int, help="Multimeter USB port number (ttyUSB*)")
@click.option("--voltage", required=True, type=int, help="Voltage value in bits (0-16383)")
def calib_measurement(board, mez, mezch, kport, voltage):
    """*Single bit calibration"""
    calib.calibration_one_measurement(board, mez, mezch, kport, voltage)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
def read_channel_volt(board, mez, mezch):
    """*Get channel voltage in volts"""
    with api.can_init(board):
        result = api.read_channel_volt(board, mez, mezch)
        channel = api.mez_mezch_converter(mez, mezch)
        print("%2d %2d %3d %4d | ADC code: %8d  | voltage: %8.4f V" % (board, mez, mezch, channel, result["ADC_code"], round(result["voltage"],4)))


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def read_channels_volt(board):
    """*Get channel voltages in volts"""
    with api.can_init(board):
        api.read_all_channel_volt(board)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--file", required=True, help="Path to the file with the voltage values on the channels")
def set_voltage_from_file(board, file):
    """*Set voltage to channels using a file"""
    with api.can_init(board):
        api.set_voltage_from_file_path(board, file)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--file", required=True, help="Path to the file with the voltage values on the channels")
def read_voltage_from_file(board, file):
    """*Read voltage to channels using a file"""
    with api.can_init(board):
        api.read_voltage_from_file_path(board, file)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
@click.option("--mez", required=True, type=int, help="Mezzanine number (0-3)")
@click.option("--mezch", required=True, type=int, help="Channel number (0-31)")
@click.option("--voltage", required=True, type=float, help="Voltage value in volts")
def correction_voltage(board, mez, mezch, voltage):
    """*Voltage correction"""
    with api.can_init(board):
        api.correction_voltage(board, mez, mezch, voltage)


@cli.command()
@click.option("--board", required=True, type=int, help="Board number")
def correction_voltage_from_file(board):
    """*Voltage correction for channels specified in the file"""
    with api.can_init(board):
        api.correction_voltage_from_file(board)


@cli.command()
def board_status():
    """*Board status"""
    api.board_status()


@cli.command()
def calib_path():
    """*Calib path"""
    api.calib_path()
