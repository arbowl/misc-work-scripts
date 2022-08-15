import serial
from time import sleep

COM = '30'
RAISE_LID = 'G0 X.1\r\n'.encode()
LOWER_LID = 'G0 X0\r\n'.encode()


def main(open):
    fixture = serial.Serial(port='COM' + COM, baudrate=115200, timeout=.1)
    sleep(1)
    while True:
        command = input('>>>')
        fixture.write(RAISE_LID if open is False else LOWER_LID)
        open = not open

main(False)
