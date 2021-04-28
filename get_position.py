import sys
import bin.config as config
import bin.cache as cache

#call using: $ python3 set_target_position 'Shade Name' 100

arguments = sys.argv

#input checks / error handling
if len(arguments) != 3:
	raise TypeError("Incorrect number of arguments specified. Should only be 2.")

try:
	shade_name = arguments[1]
	guess_position = int(arguments[2])
except:
	print("ERROR PARSING ARGUMENTS")
	raise

#input checks
if not (shade_name in config.shades.keys()):
	raise KeyError(f"Shade: {shade_name} was not found in the config file.")
elif not (0 <= guess_position and guess_position <= 100):
	raise ValueError("Shade Position must be inbetween 0 and 100.")


#saves the current position and then prints a dummy current position
position = cache.read_position(shade_name)
print(position)