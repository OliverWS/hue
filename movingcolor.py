#!/usr/bin/python
import img2colors
import hue
import colorsys
import os
import sys
import json

def processVideo(f, fps=1.0, ncolors=3, run=True, dry_run=False):
	ext = f.split(".")[-1]
	if ext == "png" or ext == "jpg":
		processFrame(f, fps=fps,ncolors=ncolors)
	else:
		while 1:
			os.system("ffmpeg -i " + f + " frame.png -y")
			processFrame("frame.png", fps=fps,ncolors=ncolors,dry_run=dry_run)
			if not run:
				break

def processFrame(f, fps=10.0,ncolors=3,dry_run=False):
	colors = img2colors.colorz(f, n=ncolors)
	print json.dumps(colors, indent=3)
	for l in hue.b.lights:
		i = hue.b.lights.index(l)
		if i >= len(colors):
			i = len(colors)-1
		r,g,b = colors[i]
		h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
		if not dry_run:
			l.transition = 10.0/fps
			l.brightness = int(v)
			l.hue = int(h*65535.0)
			l.saturation = int(255.0*s)


def main():
	dryrun = (len([x for x in sys.argv if "dry-run" in x]) > 0)
	if dryrun:
		print "Executing as dryrun"
	if len(sys.argv) == 2:
		processVideo(sys.argv[1], dry_run=dryrun)
	elif len(sys.argv) == 3:
		processVideo(sys.argv[1],ncolors = int(sys.argv[-1]),dry_run=dryrun)

if __name__ == '__main__':
	main()