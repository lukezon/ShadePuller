#############################
###Shades Dictionary Setup###
#############################

shades = {
	'TestShade':{
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

#stop settings (turn motor off)
stop_pin_1 = False
stop_pin_2 = False


######################
###General Settings###
######################

verbose = False
set_target_position_delay = 0 #seconds

polling_delay = 0.5 #seconds
motor_timeout = 15 #seconds


##########################
### Data File Settings ###
##########################

data_directory = '/home/luke/ShadePullerV2/data/'