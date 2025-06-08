import time
from pinpong.board import I2C, Board

CCS811_ADDR = 0x5A
CSS811_STATUS = 0x00
CSS811_MEAS_MODE = 0x01
CSS811_ALG_RESULT_DATA = 0x02
CSS811_RAW_DATA = 0x03
CSS811_ENV_DATA = 0x05
CSS811_NTC = 0x06
CSS811_THRESHOLDS = 0x10
CSS811_BASELINE = 0x11
CSS811_HW_ID = 0x20
CSS811_HW_VERSION = 0x21
CSS811_FW_BOOT_VERSION = 0x23
CSS811_FW_APP_VERSION = 0x24
CSS811_ERROR_ID = 0xE0
CSS811_APP_START = 0xF4
CSS811_SW_RESET = 0xFF


class CCS811:
    """
    Classe de base pour le capteur CCS811.
    """

    def __init__(self):
        Board("UNIHIKER").begin()
        self.i2c = I2C()
        self.tVOC = 0
        self.CO2 = 0

    def print_error(self):
        error = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ERROR_ID, 1)[0]
        message = 'Error: '
        if error & (1 << 5):
            message += 'HeaterSupply '
        elif error & (1 << 4):
            message += 'HeaterFault '
        elif error & (1 << 3):
            message += 'MaxResistance '
        elif error & (1 << 2):
            message += 'MeasModeInvalid '
        elif error & (1 << 1):
            message += 'ReadRegInvalid '
        elif error & (1 << 0):
            message += 'MsgInvalid '
        print(message)

    def check_for_error(self):
        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & (1 << 0)

    def app_valid(self):
        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & (1 << 4)

    def set_drive_mode(self, mode):
        if mode > 4:
            mode = 4
        setting = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_MEAS_MODE, 1)[0]
        setting &= ~(0b00000111 << 4)
        setting |= (mode << 4)
        self.i2c.writeto_mem(CCS811_ADDR, CSS811_MEAS_MODE, setting)

    def configure_ccs811(self):
        hardware_id = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_HW_ID, 1)[0]
        if hardware_id != 0x81:
            raise ValueError('CCS811 not found. Please check wiring.')
        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at Startup.')
        if not self.app_valid():
            raise ValueError('Error: App not valid.')
        self.i2c.writeto(CCS811_ADDR, bytes([CSS811_APP_START]))
        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at AppStart.')
        self.set_drive_mode(1)
        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at setDriveMode.')

    def setup(self):
        print('Starting CCS811 Read')
        self.configure_ccs811()
        result = self.get_base_line()
        print("baseline for this sensor: 0x")
        if result < 0x100:
            print('0')
        if result < 0x10:
            print('0')
        print(result)

    def get_base_line(self):
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_BASELINE, 2)
        baseline_msb = data[0]
        baseline_lsb = data[1]
        baseline = (baseline_msb << 8) | baseline_lsb
        return baseline

    def data_available(self):
        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & (1 << 3)

    def run(self):
        self.setup()
        while True:
            if self.data_available():
                self.read_logorithm_results()
                print("CO2[%d] tVOC[%d]" % (self.CO2, self.tVOC))
            elif self.check_for_error():
                self.print_error()
            time.sleep(1)

    def read_logorithm_results(self):
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ALG_RESULT_DATA, 4)
        co2_msb = data[0]
        co2_lsb = data[1]
        tvoc_msb = data[2]
        tvoc_lsb = data[3]
        self.CO2 = (co2_msb << 8) | co2_lsb
        self.tVOC = (tvoc_msb << 8) | tvoc_lsb


if __name__ == "__main__":
    c = CCS811()
    c.run()
