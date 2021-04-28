import bin.config as config
from bin.move_shade import Shade
import bin.cache as cache
import time, copy



#initiates the shade objects from config
shades = {}
for shade_name in config.shades.keys():
	shades[shade_name] = Shade(shade_name, config.shades[shade_name]['ADC Pin'], config.shades[shade_name]['Motor Pin 1'], config.shades[shade_name]['Motor Pin 2'], config.shades[shade_name]['Cutoff'])



while True:
	time.sleep(config.polling_delay)

	#goes through each shade
	for shade in shades.values():

		print('Target: ', shade.target_pos)
		print('Current: ', shade.current_pos)
		print(shade.start_time)

		#checks to make sure max current wasn't hit, if it is it stops the motor and logs new position
		if shade.check_voltage():
			shade.stop()
			#assumes that it hit the target position
			if shade.target_pos != None:
				shade.cleanup()

		#checks to make sure the shade hasn't been moving for longer than specified timeout time
		if shade.check_time(config.motor_timeout):
			shade.stop()
			#assumes that it hit the target position
			if shade.target_pos != None:
				shade.cleanup()	

		#checks for a new target position and sets to the shades target
		new_target = cache.read_target(shade_name)
		if new_target != None:
			shade.target_pos = new_target
			shade.start_time = time.time()

			if shade.target_pos == 100:
				shade.move_up()
			elif shade.target_pos == 0:
				shade.move_down()
			else:
				pass

		#logs the current shade positions to file
		cache.set_position(shade.name, shade.current_pos)