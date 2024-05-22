import sys
import sqlite3
sys.path.append('../lib/')

from myo import Myo
from print_pose_listener import PrintPoseListener
from vibration_type import VibrationType

def main():
	
	print('Start Myo for Linux');
	
	listener = PrintPoseListener()
	myo = Myo()

	try:
		myo.connect()
		print("aaaaaaaa")
		myo.add_listener(listener)
		print("bbbbbbbb")
		myo.vibrate(VibrationType.SHORT)
		print("cccccccc")
		n = 0
		while n < 2000:

			n = n+1
			myo.run()

	except KeyboardInterrupt:
		pass
	except ValueError as ex:
		print(ex)
	finally:
		myo.safely_disconnect()
		print('Finished.')

if __name__ == '__main__':
	main()
