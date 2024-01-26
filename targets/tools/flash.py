"""Script program target over openocd."""

import subprocess
import json

from rules_python.python.runfiles import runfiles
from serial.tools import list_ports
from dataclasses import dataclass
import argparse

@dataclass
class ConfigData:
    """Class for keeping information from json config file."""
    binary_path: str
    openocd_path: str
    openocd_config_path: str
    target_vendor_id: int
    target_product_id: int
    def __init__(self, json_path: str):
        r = runfiles.Create()
        with open(r.Rlocation(json_path)) as f:
            data = json.load(f)
            self.binary_path = r.Rlocation(data['BINARY_PATH'])
            self.openocd_path = r.Rlocation(data['OPENOCD_PATH'])
            self.openocd_config_path = r.Rlocation(data['OPENOCD_CONFIG_PATH'])
            self.target_vendor_id = int(data['TARGET_VENDOR_ID'], 16)
            self.target_product_id = int(data['TARGET_PRODUCT_ID'], 16)

def get_board_serial(vid, pid) -> str:
    for dev in list_ports.comports():
        if dev.vid == vid and dev.pid == pid:
            return dev.serial_number
    raise IOError("Failed to detect connected board")


def flash(config: ConfigData):

    board_serial = get_board_serial(config.target_vendor_id,
                                    config.target_product_id)

    print('\nInput Information to OpenOCD:')
    print(f'Board serial port signature: {board_serial}')
    print(f"binary Rlocation is: {config.binary_path}")
    print(f"openocd Rlocation is: {config.openocd_path}")
    print(f"openocd config Rlocation is: {config.openocd_config_path}")

    assert config.binary_path is not None
    assert config.openocd_config_path is not None
    subprocess.check_call(
        [
            config.openocd_path,
            "-f",
            f"{config.openocd_config_path}",
            "-c",
            f"program {config.binary_path} reset exit",
        ], )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()
    config_data = ConfigData(args.file)
    flash(config_data)
