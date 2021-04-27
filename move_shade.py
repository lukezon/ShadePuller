import sys, config, time
import busio, digitalio, board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


####################################
####Utility Function Definitions####
####################################

def vprint(string):
	if config.verbose:
		print(string)

def check_time(start_time):
	current_time = time.time()
	time_elapsed = current_time - start_time
	return int(time_elapsed)


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


#prints key attributes if verbose:
if config.verbose:
	print('Request Type:', request)
	print('Shade Name:', shade_name)
	print('TargetPosition', shade_position)
	print('Shade Object from Config', shade)


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


#############################################
###### Motor / Shade Control Functions ######
#############################################

def get_direction_pins(direction):
	"""Gets the pin settings for upward/downward motion from config"""
	direction = direction.lower()

	if direction == 'up':
		return config.up_pin_1, config.up_pin_2
	elif direction == 'down':
		return config.down_pin_1, config.down_pin_2
	elif direction == 'stop':
		return config.stop_pin_1, config.stop_pin_2
	else:
		raise NotImplementedError('Direction must be either UP or DOWN')


def check_voltage(sensor_object, cutoff):
	"""Checks the ADC voltage VS the cuttoff, returns True if voltage >= cutoff voltage"""
	vprint(f'Raw ADC Value: {sensor.value}')
	if sensor_object.value >= cutoff:
		vprint(f"HIT ADC voltage cuttoff. [ADC = {sensor_object.value}, Cutoff = {cutoff}]")
		return True
	else:
		return False


def move_shade(direction, TargetPosition, pin_1_object, pin_2_object, sensor_object, cutoff):
	#input sterilization
	direction = direction.lower()
	#temporary check to make sure that the given input is valid
	if direction == 'up' and TargetPosition == 100:
		pass
	elif direction == 'down' and TargetPosition == 0:
		pass
	else:
		print("ERROR: Setting shade to intermediate positions not yet implemented")
		return False

	#turns on the motor in the correct direction
	vprint("Turning on Motor...")
	pin_1_object.value, pin_2_object.value = get_direction_pins(direction)

	#stop logic for setting shade to position 0 or 100
	if TargetPosition == 0 or TargetPosition == 100:
		
		#checks the sense voltage, stops the motors once a cirtain threshold is met or timeout is hit
		moving = True
		error = False
		start_time = time.time()

		while moving:
			time.sleep(config.sensor_poll_delay)

			motor_stopped = check_voltage(sensor_object, cutoff)
			time_elapsed = check_time(start_time)

			if motor_stopped:
				vprint(f'Motor Movement Complete. \nTime Elapsed: {time_elapsed} seconds')
				moving = False
			elif time_elapsed >= config.motor_timeout:
				vprint(f'ERROR: Motor Timeout ({time_elapsed}) hit.')
				error = True
				moving = False


	#stops the motors (cuts off power)
	vprint("Turning off Motor...")
	pin_1_object.value, pin_2_object.value = get_direction_pins('stop')

	if error:
		return False
	else:
		return True


###################################
###### Motor / Shade Control ######
###################################

success = move_shade(request, shade_position, motor_1, motor_2, sensor, shade['Cutoff'])

if (not success) and config.raise_exeption_on_movement_error:
	vprint('Encountered an error during motor movement.')
	raise Exception('MOTOR MOVEMENT FAILURE')


print("Done.")
