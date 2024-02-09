from machine import UART, Pin, I2C
from dht import DHT11
from pico_i2c_lcd import I2cLcd
import utime

# UART setup for pH sensor
uart = UART(0, baudrate=9600, rx=Pin(1))

# DHT11 setup
dht_pin = Pin(2, Pin.IN)
dht = DHT11(dht_pin)

# I2C setup for LCD
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def read_ph_value():
    for _ in range(10):
        ph_data = uart.readline().decode('utf-8').strip()
        if "PH:" in ph_data:
            ph_value = float(ph_data.split("PH:")[1].split(",")[0])
            return ph_value - 2

    return None

def read_dht_value():
    dht.measure()
    temperature = dht.temperature()
    humidity = dht.humidity()
    return temperature, humidity

def display_lcd(ph_value, temperature, humidity):
    lcd.clear()
    #lcd.move_to(0, 0)
    lcd.putstr("pH: {:.2f}".format(ph_value))
    utime.sleep(1)
    #lcd.move_to(0, 1)
    lcd.clear()
    lcd.putstr("Temp: {:.1f}C, Hum: {:.1f}%".format(temperature, humidity))
    utime.sleep(1)

while True:
    try:
        ph_value = read_ph_value()
        temperature, humidity = read_dht_value()

        if ph_value is not None:
            display_lcd(ph_value, temperature, humidity)

    except Exception as e:
        print("Error:", e)

    # Wait for a few seconds before the next reading
    utime.sleep(2)

