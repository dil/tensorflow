import subprocess
import os
import re
import sys
import tempfile
import argparse

# Go through the cars directories, and if any car has fewer than 500 cars, boost the number by
# - rotate 90, 180, 270
# - mirror vertically, horizontally
rotations = ['d90', 'd180', 'd270']
flips = ['vertical', 'horizontal']
zooms = ['2']
zoomCrops = ["256 256 512 512", "0 0 512 512", "0 512 512 512", "512 0 512 512", "512 512 512 512", "0 256 512 512", "256 0 512 512", "0 128 512 512", "128 0 512 512", "128 128 512 512"]
targetNumberOfCars = 500

parser = argparse.ArgumentParser()
parser.add_argument(
	'--image_dir',
	type=str,
	default='',
	help='Path to folders of images.'
)
FLAGS, unparsed = parser.parse_known_args()
carDir = FLAGS.image_dir
cars = os.listdir(carDir)

for index,car in enumerate(cars):
	cars = [f for f in os.listdir(carDir+car) if not re.match(r'.*-rot-.*.jpg', f) and not re.match(r'.*-flip-.*.jpg', f) and not re.match(r'.*-zoom-.*.jpg', f)] # filter transformed car file names
	# rotate
	for rotation in rotations:
		totalNumberOfCars = len(os.listdir(carDir+car)) # including originals and boosting variations
		if totalNumberOfCars <= targetNumberOfCars:
			print("{} of {}: {} has {}, boosting with rotation {}".format(index+1, len(cars), car, totalNumberOfCars, rotation))
			for p in cars:
				src = carDir+car+'/'+p
				dst = carDir+car+'/'+p.split('.')[0]+'-rot-'+rotation+'.'+p.split('.')[1]
				subprocess.call("vips rot '{}' '{}' {}".format(src, dst, rotation), shell=True)
	# flip
	for flip in flips:
		totalNumberOfCars = len(os.listdir(carDir+car)) # including originals and boosting variations
		if totalNumberOfCars <= targetNumberOfCars:
			print("{} of {}: {} has {}, boosting with flip {}".format(index+1, len(cars), car, totalNumberOfCars, flip))
			for p in cars:
				src = carDir+car+'/'+p
				dst = carDir+car+'/'+p.split('.')[0]+'-flip-'+flip+'.'+p.split('.')[1]
				subprocess.call("vips flip '{}' '{}' {}".format(src, dst, flip), shell=True)
	# zoom
	for zoom in zooms:
		totalNumberOfCars = len(os.listdir(carDir+car)) # including originals and boosting variations
		if totalNumberOfCars <= targetNumberOfCars:
			tmppath = tempfile.mkdtemp()  # need a temp path because we have to do two operations on the file
			print("{} of {}: {} has {}, boosting with zoom {}".format(index+1, len(cars), car, totalNumberOfCars, zoom))
			for p in cars:
				src = carDir+car+'/'+p
				for idx,zoomCrop in enumerate(zoomCrops):
					newFileName = p.split('.')[0]+'-zoom-'+zoom+'-'+str(idx+1)+'.'+p.split('.')[1]
					tmp = tmppath +'/'+newFileName
					dst = carDir+car+'/'+newFileName
					subprocess.call("vips zoom '{}' '{}' {} {}".format(src, tmp, zoom, zoom), shell=True)  # doubles the dimensions of the image
					subprocess.call("vips extract_area '{}' '{}' {}".format(tmp, dst, zoomCrops[idx]), shell=True)  # so we need to crop it again
	# check the number we ended up with
	totalNumberOfCars = len(os.listdir(carDir+car))
	if totalNumberOfCars <= targetNumberOfCars:
		print("WARNING: {} has {} cars".format(car, totalNumberOfCars))


