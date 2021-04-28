import os
import bin.config as config

data_directory = config.data_directory

def set_target(shade_name, position):
	"""Writes the target position to the proper dat file"""
	with open(f'{data_directory}{shade_name}_target.dat', 'w') as file:
		file.write(str(position))
	return

def read_target(shade_name):
	"""Reads the target position from the proper dat file then deletes the file"""
	try:
		with open(f'{data_directory}{shade_name}_target.dat', 'r') as file:
			target_position = int(file.read())
		os.remove(f'{data_directory}{shade_name}_target.dat')
	except:
		target_position = None

	return target_position


def set_position(shade_name, position):
	"""writes the current position of the shade to file"""
	with open(f'{data_directory}{shade_name}_current.dat', 'w') as file:
		file.write(str(position))
	return

def read_position(shade_name):
	"""Reads the current position from the proper dat file"""
	try:
		with open(f'{data_directory}{shade_name}_current.dat', 'r') as file:
			position = int(file.read())
	except:
		position = 0

	return position


