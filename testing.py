import time, sys


arguments = sys.argv

print(arguments)





demo = 0
while demo < 15:
	demo += 1
	print('MOVING')
	time.sleep(1)

print('DONE')
