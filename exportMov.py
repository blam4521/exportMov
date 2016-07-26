import os, sys
import os.path
from os.path import isfile, join
import os.path
import ffmpy
import time
import datetime
import logging

## ----------------------------------------------------------------------

def find_missing( list_path ):
	''' Checks to see if sequence has missing frames '''

	# Turn files list_path in a str list
	string_list = ([f for f in os.listdir(list_path) if os.path.isfile(join(list_path, f))])
	
	string_num = []	

	# Split the strings, by '.' to isolate sequence numbers
	for i in string_list:
	    m = i.split('.')[1]
	    string_num.append(m)
	    #print m

	# Turn string_numbers into int numbers	    
	int_num = [ int(i) for i in string_num ]
	#print("Intger list is %s"%int_num)

	# Finds missing values if they're are missing frames
	missing = []
	for i in range(1, max(int_num)):
	    if not i in int_num:
	        missing.append(i)

	print("Missing frames are: %s"%missing)

	#print len(missing)

	return (missing)

## ----------------------------------------------------------------------


def export_mov( baseFile, outputPath ):
	''' Exports image seq to mpeg4 format '''
	
	# Example ffmeg cmd:
	# ffmpeg -f image2 -r 1/5 -i image%05d.png -vcodec mpeg4 -y movie.mp4

	#index = 0
	t = time.localtime()
	#saveFile = str("test.%04d"%(index)) + ".mov"
	timestamp = time.strftime('%y-%b-%d_%H-%M', t)
	saveFile = "Shot_%s"%timestamp + ".mov"

	extension = '/'.join( [outputPath, saveFile] )   
	print("The full extension is: %s"%extension)

	# Inputs and outputs for seq to mov convert

	ff = ffmpy.FFmpeg(
		inputs= { baseFile : None },
		#outputs={ outputPath : '-r 24 -vcodec mpeg4 -c: libx264' }
		outputs={ extension : '-r 24 -vcodec mpeg4' }
	)
	print ("results of ff%s"%ff)
	# Displays the command for ffmpeg
	#command_line = ff.cmd
	#print("This is the output for %s:"%command_line)
	
	# Runs FFmpeg
	ff.run()
	print("...Finshed Converting Seq To Mov Format")
	
	return(1)
	
## ----------------------------------------------------------------------


def main( basePath, file_image_format ):
	''' Input basePath and image format 
	# This path is for testing 
	purposes:list_path = basePath + "\test_frames_list"

	# This path is for testing purposes for file image format:
	# baseFile = "C:\Users\Bears\Documents\maya\projects\Chinatown_Level\images\complete_frames_list\CLOTH01A_001.%04d.png"

	# Example of file_image_format input:
	# CLOTH01A_001.%04d.png
	'''

	baseFile = basePath + "\\" + file_image_format  

	outputPath = basePath + "\MovFiles"

	if not os.path.exists( outputPath ):
		print( "Making directory:", outputPath )
		make = os.makedirs( outputPath )
		print( "This is the directory created %s"%make )
	else:
		print( "Directory already exists", outputPath )
		
	# Checks if the frames are not missing	
	if len(find_missing(basePath)) > 0:
		print("...Can't perform conversion")
	else:
		print("Convertng PNGS to MOV...")
		export_function = export_mov( baseFile, outputPath )
	

## ----------------------------------------------------------------------

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
	#main()