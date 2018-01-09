# -*- coding:utf8 -*-
import csv
import os


def getMedium(data):
	if len(data)<3:
		print "the data is too small"
		return
	total = 0
	data = sorted(data)
	if len(data)%2 ==0:
		index = len(data)/2
		medium = (data[index] + data[index-1])/2
	else:
		index = len(data)/2
		medium = data[index+1]
	print "the medium is "+str(medium)
	for item in data:
		total +=item
	print "the avg is "+str(total/len(data))

def getrange(data):
	ret = dict()
	for item in data:
		num = item/30
		if num in ret:
			ret[num] +=1
		else:
			ret[num] = 1
	config_file = "./range_config/ni-night.csv"
	file = open(config_file,"w")
	write_lines = []
	for item in ret:
		tmp = str(30*item) + " - " + str(30*item + 29)
		line = tmp + " : "+ str(ret[item]) + '\n'
		write_lines.append(line)
		# print int(line.split(":")[0].split('-')[0])
	write_lines = sorted(write_lines, key=lambda tick_data : int(tick_data.split(":")[0].split('-')[0]))
	file.writelines(write_lines)
	file.close()
	print "has write the config file"


def getData(path):
	ret = []
	f = open(path)
	for line in f:
		line =  line.strip()
		ret.append(int(line))
	return ret

def main():
	path = "./ni/ni-night.txt"
	data = getData(path)
	getrange(data)
	getMedium(data)


if __name__ == '__main__':
	main()