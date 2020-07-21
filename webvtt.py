#webvtt.py
import sys

from webvttUtils import *

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f:
	data = writeTranscriptToWebVTT(f.read(), 'en', output_file )