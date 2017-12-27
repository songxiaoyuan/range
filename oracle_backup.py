import cx_Oracle  
import os
import csv
import time
#!/usr/bin/python
# -*- coding:utf8 -*-

def writefile(result,filename):
	# print "start to write the file "+filename
	instrumentid = filename.split('_')[0]
	# create the filename
	path1 = "data/"+instrumentid
	if os.path.exists(path1):
		pass
	else:
		os.makedirs(path1)
	# start write the file
	path = "data/"+instrumentid +'/'+ filename+".csv"
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(result)
	csvfile.close()


def getSortedData(data):
	ret = []
	night = []
	zero = []
	day = []
	nightBegin = 21*3600
	nightEnd = 23*3600+59*60+60
	zeroBegin = 0
	zeroEnd = 9*3600 - 100
	dayBegin = 9*3600
	dayEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		try:
			nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		except Exception as e:
			nowTime = 0
		

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			zero.append(line)
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			day.append(line)
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			night.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	night = sorted(night, key = lambda x: (x[20], int(x[21])))
	zero = sorted(zero, key = lambda x: (x[20], int(x[21])))
	day = sorted(day, key = lambda x: (x[20], int(x[21])))
	for line in night:
		ret.append(line)
	for line in zero:
		ret.append(line)
	for line in day:
		ret.append(line)

	return ret


def getOneDict(data):
	ret = set()
	for line in data:
		if len(line) >=1:
			ret.add(line[0])
	return ret


def main():
	instrumentid_set = dict()
	conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')   
	cursor = conn.cursor () 

	# print "start get all the instrumentid"
	# mysql="select INSTRUMENTID from hyqh.quotatick where TRADINGDAY = '20171127'"
	# print mysql
	# cursor.execute (mysql)  

	# icresult = cursor.fetchall()
	# print "has get the data"
	# instrumentid_set = getOneDict(icresult)
	# print len(instrumentid_set)
	instrumentid_set = {"ru1805","ru1801"}

	print "start get all the date"
	mysql="select TRADINGDAY from hyqh.quotatick  where INSTRUMENTID = 'ru1801'"
	print mysql
	cursor.execute (mysql)  

	icresult = cursor.fetchall()
	tradingday_set = getOneDict(icresult)
	print len(tradingday_set)

	print "start to get all the file"
	for instrumentid in instrumentid_set:
		for day in tradingday_set:
			mysql="select * from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s' " % (day,instrumentid)

			cursor.execute (mysql)
			icresult = cursor.fetchall()
			cleandata = getSortedData(icresult)
			filename = instrumentid + "_" + day

			writefile(cleandata,filename)

	cursor.close ()  
	conn.close () 


if __name__=='__main__': 
	main()
	# data = [[1],[2],[3]]
	# filename = "rb1801_20170926"
	# writefile(data,filename)