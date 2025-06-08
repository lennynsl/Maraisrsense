import time
from pinpong.board import I2C, Board

CCS811_ADDR = 0x5A
CCS811_ALG_RESULT_DATA = 0x02

def main():
    Board("UNIHIKER").begin()
    i2c = I2C()

    while True:
        # Lecture de 4 octets à partir du registre 0x02 (trame standard CCS811)
        data = i2c.readfrom_mem(CCS811_ADDR, CCS811_ALG_RESULT_DATA, 4)
        co2 = (data[0] << 8) | data[1]
        tvoc = (data[2] << 8) | data[3]
        print(f"CO₂: {co2} ppm | TVOC: {tvoc} ppb")
        time.sleep(10)

if __name__ == "__main__":
    main()