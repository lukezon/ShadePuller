import sys, config, time
import busio, digitalio, board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


#############################################
####Command Line Argument / Input Parsing####
#############################################
# example: $ python3 move_shade.py 'up' 'Shade Name, str' 'Shade Position (int, 0-100)'

arguments = sys.argv

#checks for stop command
if arguments[0] == 'stop':
	print("RECEIVED STOP COMMAND")
	exit()

#input checks / error handling
elif len(arguments) != 4:
	raise TypeError("Incorrect number of arguments specified. Should only be 2. Ex. $ python3 move_shade.py 'Shade Name, str' 'Shade Position (int, 0-100)'")

try:
	request = arguments[1]
	shade_name = arguments[2]
	shade_position = int(arguments[3])
except:
	print("ERROR PARSING ARGUMENTS")
	raise

if not (shade_name in config.shades.keys()):
	raise KeyError(f"Shade: {shade_name} was not found in the config file.")
elif not (0 <= shade_position and shade_position <= 100):
	raise ValueError("Shade Position must be inbetween 0 and 100.")

#gets the shade info from config
shade = config.shades[shade_name]


#############################################
#### RPI GPIO Setup / MCP3008 Chip Setup ####
#############################################

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin from config
sensor_pin = getattr(MCP, f"P{shade['ADC Pin']}")
sensor = AnalogIn(mcp, sensor_pin)

#sets up the motor digital pins
motor_1 = getattr(board, f"D{shade['Motor Pin 1']}")
motor_2 = getattr(board, f"D{shade['Motor Pin 2']}")
motor_1 = digitalio.DigitalInOut(motor_1)
motor_2 = digitalio.DigitalInOut(motor_2)
motor_1.direction = digitalio.Direction.OUTPUT
motor_2.direction = digitalio.Direction.OUTPUT

print('Raw ADC Value: ', sensor.value)
print('ADC Voltage: ' + str(sensor.voltage) + 'V')

motor_1.value, motor_2.value = True, True
time.sleep(5)
motor_1.value, motor_2.value = False, False

print("Done")
