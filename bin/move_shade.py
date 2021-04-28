import time
import bin.config as config
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
#### RPI GPIO Setup / MCP3008 Chip Setup ####
#############################################

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)


#############################################
###### Motor / Shade Control Functions ######
#############################################

class Shade():

	def __init__(self, name, adc_pin, motor_1, motor_2, cutoff):
		"""
		Initiates the shade object.
		name = name of the shade
		adc_pin = int. from 0-7 representing the pin on the ADC
		motor_1 = int. GPIO pin corresponding to control pin 1 for motor controller
		motor_2 = int. GPIO pin corresponding to control pin 2 for motor controller
		cutoff = the raw cutoff value for the ADC
		"""

		# create an analog input channel on pin from config
		adc_pin = getattr(MCP, f"P{adc_pin}")
		self.sensor = AnalogIn(mcp, adc_pin)

		#sets up the motor digital pins
		motor_1 = getattr(board, f"D{motor_1}")
		motor_2 = getattr(board, f"D{motor_2}")
		self.motor_1 = digitalio.DigitalInOut(motor_1)
		self.motor_2 = digitalio.DigitalInOut(motor_2)
		self.motor_1.direction = digitalio.Direction.OUTPUT
		self.motor_2.direction = digitalio.Direction.OUTPUT

		#initiates variables
		self.name = name
		self.cutoff = cutoff
		self.current_pos = 0
		self.target_pos = None
		self.start_time = None

	def check_voltage(self):
		"""Checks the ADC voltage VS the cuttoff, returns True if voltage >= cutoff voltage"""
		vprint(f'Raw ADC Value: {self.sensor.value}')
		if self.sensor.value >= self.cutoff:
			vprint(f"HIT ADC voltage cuttoff. [ADC = {self.sensor.value}, Cutoff = {self.cutoff}]")
			return True
		else:
			return False

	def check_time(self, duration):
		"""checks to make sure the timeout time hasn't been reached"""
		if self.start_time == None: #returns false if no start time saved in object
			return False
		if (time.time() - self.start_time) >= duration:
			return True
		else:
			return False

	def cleanup(self):
		"""should be called when a movement is finished to cleanup the target position, current position, and start time variables"""
		self.current_pos = self.target_pos
		self.target_pos = None
		self.start_time = None

	def move_up(self):
		"""moves the shade upwards DOES NOT STOP AUTOMATICALLY"""
		self.motor_1.value, self.motor_2.value = config.up_pin_1, config.up_pin_2

	def move_down(self):
		"""moves the shade downwards DOES NOT STOP AUTOMATICALLY"""
		self.motor_1.value, self.motor_2.value = config.down_pin_1, config.down_pin_2

	def stop(self):
		"""Stops the motor"""
		self.motor_1.value, self.motor_2.value = config.stop_pin_1, config.stop_pin_2



#############################################
###### Motor / Shade Control Functions ######
#############################################



# def move_shade(direction, TargetPosition, pin_1_object, pin_2_object, sensor_object, cutoff):
# 	#input sterilization
# 	direction = direction.lower()
# 	#temporary check to make sure that the given input is valid
# 	if direction == 'up' and TargetPosition == 100:
# 		pass
# 	elif direction == 'down' and TargetPosition == 0:
# 		pass
# 	else:
# 		vprint("ERROR: Setting shade to intermediate positions not yet implemented")
# 		return False

# 	#turns on the motor in the correct direction
# 	vprint("Turning on Motor...")
# 	pin_1_object.value, pin_2_object.value = get_direction_pins(direction)

# 	#stop logic for setting shade to position 0 or 100
# 	if TargetPosition == 0 or TargetPosition == 100:
		
# 		#checks the sense voltage, stops the motors once a cirtain threshold is met or timeout is hit
# 		moving = True
# 		error = False
# 		start_time = time.time()

# 		while moving:
# 			time.sleep(config.sensor_poll_delay)

# 			motor_stopped = check_voltage(sensor_object, cutoff)
# 			time_elapsed = check_time(start_time)
# 			print(100)
# 			if motor_stopped:
# 				vprint(f'Motor Movement Complete. \nTime Elapsed: {time_elapsed} seconds')
# 				moving = False
# 			elif time_elapsed >= config.motor_timeout:
# 				vprint(f'ERROR: Motor Timeout ({time_elapsed}) hit.')
# 				error = True
# 				moving = False


# 	#stops the motors (cuts off power)
# 	vprint("Turning off Motor...")
# 	pin_1_object.value, pin_2_object.value = get_direction_pins('stop')

# 	if error:
# 		return False
# 	else:
# 		return True


# ###################################
# ###### Motor / Shade Control ######
# ###################################

# success = move_shade(request, shade_position, motor_1, motor_2, sensor, shade['Cutoff'])

# if (not success) and config.raise_exeption_on_movement_error:
# 	vprint('Encountered an error during motor movement.')
# 	raise Exception('MOTOR MOVEMENT FAILURE')

# new_position = shade_position

# print(new_position)
