from machine import UART, Pin, I2C
from dht import DHT11
from pico_i2c_lcd import I2cLcd
import utime
import urequests
import vaibhav

# UART setup for pH sensor
uart = UART(0, baudrate=9600, rx=Pin(1))

# DHT11 setup
dht_pin = Pin(2, Pin.IN)
dht = DHT11(dht_pin)

# I2C setup for LCD
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# GPIO pin setup for LED
led_pin = Pin(25, Pin.OUT)

# Function to read pH value from the sensor
def read_ph_value():
    for _ in range(1):
        ph_data = uart.readline().decode('utf-8').strip()
        if "PH:" in ph_data:
            ph_value = float(ph_data.split("PH:")[1].split(",")[0])
            return ph_value - 0.28 *ph_value
    return None

# Function to read temperature and humidity from DHT11 sensor
def read_dht_value():
    dht.measure()
    temperature = dht.temperature()
    humidity = dht.humidity()
    return temperature, humidity

# Function to display data on LCD
def display_lcd(ph_value, temperature, humidity,result):
    lcd.clear()
    lcd.putstr("pH: {:.2f}".format(ph_value))
    utime.sleep(1)
    lcd.clear()     
    lcd.putstr("Temp: {:.1f}C      Hum: {:.1f}%".format(temperature, humidity))
    utime.sleep(1)
    lcd.clear()
    lcd.putstr(f"Crop_prediction:{result}")
    utime.sleep(2)
    lcd.clear()

# Function to send data to vaibhav.score API and receive the response
def send_data_to_api(data):
    return vaibhav.score(data)

def display_info():
    lcd.clear()
    lcd.putstr('LOADING ...')
    utime.sleep(1)
    lcd.clear()
    lcd.putstr("Welcome to      ")
    lcd.putstr(f"CROP PREDICTOR")
    utime.sleep(2)
    lcd.clear()
    
    utime.sleep(2)
    lcd.clear()
# Function to control LED based on API result
def control_led(result):
    if result is not None:
        led_pin.on()
    else:
        led_pin.off()
display_info()
while True:
    try:
        # Read sensor values
        ph_value = read_ph_value()
        temperature, humidity = read_dht_value()

        if ph_value is not None:
            # Display data on LCD
            

            # Create a list with sensor data
            sensor_data = [
                temperature, humidity,ph_value,160

            ]

            # Send data to vaibhav.score API
            api_response = send_data_to_api(sensor_data)

            if api_response is not None:
                # Store the response in a variable and print it
                result = api_response
                print("PREDICTION :", result)
                display_lcd(ph_value, temperature, humidity,result)
                print(ph_value)
                # Control LED based on API result
                control_led(result)

    except Exception as e:
        print("Error:", e)

    # Wait for a few seconds before the next reading
    utime.sleep(2)
