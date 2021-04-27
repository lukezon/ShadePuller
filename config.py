#############################
###Shades Dictionary Setup###
#############################

shades = {
	'Test Shade':{
		'ADC Pin': 0,
		'Motor Pin 1': 2,
		'Motor Pin 2': 3,
		'Cutoff': 10000
	}
}


###############################
###Motor Controller Settings###
###############################

#move up settings
up_pin_1 = True
up_pin_2 = False

#move down settings
down_pin_1 = False
down_pin_2 = True

#stop settings
stop_pin_1 = False
stop_pin_2 = False


######################
###General Settings###
######################

verbose = True
sensor_poll_delay = 0.5 #seconds
motor_timeout = 10 #seconds
raise_exeption_on_movement_error = False