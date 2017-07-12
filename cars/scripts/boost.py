import subprocess
import os
import re
import sys
import tempfile

# Go through the articts directories, and if any artist has fewer than 30 paintings, boost the number to more than 30 by
# - rotate 90, 180, 270
# - mirror vertically, horizontally
rotations = ['d90', 'd180', 'd270']
flips = ['vertical', 'horizontal']
zooms = ['2']
zoomCrops = ["256 256 512 512", "0 0 512 512", "0 512 512 512", "512 0 512 512", "512 512 512 512", "0 256 512 512", "256 0 512 512", "0 128 512 512", "128 0 512 512", "128 128 512 512"]
artistDir = "./train/artists/"
artists = os.listdir(artistDir)
targetNumberOfPaintings = 100

for index,artist in enumerate(artists):
	paintings = [f for f in os.listdir(artistDir+artist) if re.match(r'[0-9]+.jpg', f)]  # only look for the original painting file names
	# rotate
	for rotation in rotations:
		totalNumberOfPaintings = len(os.listdir(artistDir+artist)) # including originals and boosting variations
		if totalNumberOfPaintings <= targetNumberOfPaintings:
			print("{} of {}: {} has {}, boosting with rotation {}".format(index+1, len(artists), artist, totalNumberOfPaintings, rotation))
			for p in paintings:
				src = artistDir+artist+'/'+p
				dst = artistDir+artist+'/'+p.split('.')[0]+'-rot-'+rotation+'.'+p.split('.')[1]
				subprocess.getoutput("vips rot {} {} {}".format(src, dst, rotation))
	# flip
	for flip in flips:
		totalNumberOfPaintings = len(os.listdir(artistDir+artist)) # including originals and boosting variations
		if totalNumberOfPaintings <= targetNumberOfPaintings:
			print("{} of {}: {} has {}, boosting with flip {}".format(index+1, len(artists), artist, totalNumberOfPaintings, flip))
			for p in paintings:
				src = artistDir+artist+'/'+p
				dst = artistDir+artist+'/'+p.split('.')[0]+'-flip-'+flip+'.'+p.split('.')[1]
				subprocess.getoutput("vips flip {} {} {}".format(src, dst, flip))
	# zoom
	for zoom in zooms:
		totalNumberOfPaintings = len(os.listdir(artistDir+artist)) # including originals and boosting variations
		if totalNumberOfPaintings <= targetNumberOfPaintings:
			tmppath = tempfile.mkdtemp()  # need a temp path because we have to do two operations on the file
			print("{} of {}: {} has {}, boosting with zoom {}".format(index+1, len(artists), artist, totalNumberOfPaintings, zoom))
			for p in paintings:
				src = artistDir+artist+'/'+p
				for idx,zoomCrop in enumerate(zoomCrops):
					newFileName = p.split('.')[0]+'-zoom-'+zoom+'-'+str(idx+1)+'.'+p.split('.')[1]
					tmp = tmppath +'/'+newFileName
					dst = artistDir+artist+'/'+newFileName
					subprocess.getoutput("vips zoom {} {} {} {}".format(src, tmp, zoom, zoom))  # doubles the dimensions of the image
					subprocess.getoutput("vips extract_area {} {} {}".format(tmp, dst, zoomCrops[idx]))  # so we need to crop it again
	# check the number we ended up with
	totalNumberOfPaintings = len(os.listdir(artistDir+artist))
	if totalNumberOfPaintings <= targetNumberOfPaintings:
		print("WARNING: {} has {} paintings".format(artist, totalNumberOfPaintings))

