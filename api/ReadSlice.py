""""
Read a slice of Seismic Data 
Lei Huang
08/30/2015
"""

import struct
import json
import numpy as np
import sys, getopt

from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.palettes import brewer

import pandas as pd
from bokeh.charts import HeatMap

class NumpyAwareJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			if obj.ndim == 1:
				return obj.tolist()
			else:
				return [self.default(obj[i]) for i in range(obj.shape[0])]
		return json.JSONEncoder.default(self, obj)

def readSlice(name,dim,num):
	print ("start reading ", dim, num)
	try:
		f = open(name,"rb")
	except:
		print ("cannot open file", name)
		return
	try:
		byte4 = f.read(4)
		z = struct.unpack('>I',byte4)[0]
		byte4 = f.read(4)
		x = struct.unpack('>I',byte4)[0]
		byte4 = f.read(4)
		y = struct.unpack('>I',byte4)[0]
		print ("x,y,z", x,y,z)
		if dim == 'i': # inline
			I,J = x,z
		elif dim == 'x': # crossline
			I,J = y,z
		elif dim == 'z':  # z slice
			I,J = y,x
		else:
			print ('unrecoganized dimension')
			return
		print ("I, J = ", I, J)
		matrix = np.zeros((I,J),dtype=np.float32)
		

		if dim == 'i':  #inline
			f.seek((num-1)*I*J*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					matrix[i][j] = value
				#print i, matrix[i]	
		elif dim == 'x':  # crossline
			f.seek((num-1)*z*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					matrix[i][j] = value
				f.seek((x-1)*z*4, 1)
		else: # must be Z slice
			f.seek((num-1)*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					matrix[i][j] = value
					f.seek((z-1)*4, 1)


	finally:
		f.close()

	# try:
	# 	f = open("line.data","wb")
	# except:
	# 	print "cannot open line.data to write"
	# 	return
	# try:
	# 	f.write(matrix)
	# finally:
	# 	f.close()

	return I, J, matrix

def readSliceToJson(filename, dim, lineNum):
	I, J, results = readSlice(filename,dim,lineNum)
	j=json.dumps({"I": I, "J": J, "data": results},cls=NumpyAwareJSONEncoder)
	return j

def usage():
	print ('ReadSlice -i <inputfile> -d <dimension> -n <number> -o <outputfile>')

def main(argv):
	inputfile = ''
	outputfile = 'data.json'
	dim = ''
	num = -1
	try:
		opts, args = getopt.getopt(argv,"hi:d:n:o:",["ifile=","dim=","num=","ofile="])
		if not opts:
			print ('No options supplied')
			usage()
			sys.exit(2)
	except getopt.GetoptError as e:
		print (e);
		usage()
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-d", "--dim"):
			dim = arg
		elif opt in ("-n", "--num"):
			num = int(arg)
		else:
			print ("invalid arguments")
			usage()
			sys.exit(2)
	if inputfile == '' or dim == '' or num == -1:
		print ("invalid arguments")
		usage()
		sys.exit(2)
	print (inputfile, outputfile, dim, num)
	j=readSliceToJson(inputfile, dim, num)
	f=open(outputfile,"w")
	f.write(j)
	f.close()

if __name__ == "__main__":
    main(sys.argv[1:])


def readSliceBokeh(name,dim,num, req_data_id):
	print ("start reading ", dim, num)
	try:
		f = open(name,"rb")
	except:
		print ("cannot open file", name)
		return
	try:
		byte4 = f.read(4)
		z = struct.unpack('>I',byte4)[0]
		byte4 = f.read(4)
		x = struct.unpack('>I',byte4)[0]
		byte4 = f.read(4)
		y = struct.unpack('>I',byte4)[0]
		print ("x,y,z", x,y,z)
		if dim == 'i': # inline
			I,J = x,z
		elif dim == 'x': # crossline
			I,J = y,z
		elif dim == 'z':  # z slice
			I,J = y,x
		else:
			print ('unrecoganized dimension')
			return
		print ("I, J = ", I, J)
		matrix = np.zeros((I,J),dtype=np.float32)

		# Original
		# colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
		# "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]

		# Dr Huang's 
		#colors = ["#220E1E", "#131160", "#103579", "#116A74", "#11944A",
		#"#1EB911", "#63CE11", "#C9D611", "#F9DDB5", "#FFF0E4"]

		# Bokeh pallettes
		colors = brewer["Spectral"][11]
		
		x_hov = []
		y_hov = []
		sRate = []

		if dim == 'i':  #inline
			name = "front-view"
			f.seek((num-1)*I*J*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					x_hov.append(i)
					y_hov.insert(0, j) 
					sRate.append(value)

				#print i, matrix[i]	
		elif dim == 'x':  # crossline
			name = "side-view"
			f.seek((num-1)*z*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					x_hov.append(i)
					y_hov.insert(0, j) 
					sRate.append(value)
				f.seek((x-1)*z*4, 1)
		else: # must be Z slice
			name = "top-view"
			f.seek((num-1)*4, 1)
			for i in range(0,I):
				for j in range(0,J):
					byte4 = f.read(4)
					value = struct.unpack('>f',byte4)[0]
					x_hov.append(i)
					y_hov.insert(0, j) 
					sRate.append(value)
					f.seek((z-1)*4, 1)
	finally:
		f.close()

	title = req_data_id + '		dimention: ' + dim + '		number: ' + str(num) + '	' + name

	# TOOLS = "save,pan,box_zoom,hover,wheel_zoom,undo,redo,reset, resize"

	data = {'x': x_hov,
	'value': sRate,
	'y': y_hov}

	p = HeatMap(data, x='x', y='y', values='value',
		title=title, stat=None, hover_tool=True, palette=colors, legend="top_right",
		width=I*3, height=J*3
		)

	p.x_range.start = 0
	p.x_range.end = I+60
	p.y_range.start = 0
	p.y_range.end = J

	# p.select_one(HoverTool).tooltips = [
	# 	('Coordinate', '(@x, @y)'),
	# 	('Magnitute', '@values{1.11111111111111111}'),
	# ]

	return p

