# -*- coding:utf8 -*-
import csv
import os
import cx_Oracle  
import xlrd
from xlrd import xldate_as_tuple 

nameDict = {
	"rb":{"tick":1,"config_file":"rb"},
	"ru":{"tick":5,"config_file":"ru"},
	"zn":{"tick":5,"config_file":"zn"},
	"cu":{"tick":10,"config_file":"cu"},
	"hc":{"tick":1,"config_file":"hc"},
	"ni":{"tick":10,"config_file":"ni"},
	"al":{"tick":5,"config_file":"al"},
	"au":{"tick":0.05,"config_file":"au"},
	"ag":{"tick":1,"config_file":"ag"},
	"pp":{"tick":1,"config_file":"pp"},
	"v":{"tick":5,"config_file":"v"},
	"bu":{"tick":2,"config_file":"bu"},
	"pb":{"tick":5,"config_file":"pb"}
}

class GetRange(object):
	"""docstring for GetRange"""
	def __init__(self,param_dic):
		super(GetRange, self).__init__()

		self._day_max_lastprice = 0
		self._day_min_lastprice = 0
		self._night_max_lastprice = 0
		self._night_min_lastprice = 0
		self._total_max_lastprice = 0
		self._total_min_lastprice = 0

		self._tick = param_dic["tick"]
		self._config_file_day = param_dic["config_file"] + "_day"
		self._config_file_night = param_dic["config_file"] + "_night"
		self._config_file_total = param_dic["config_file"] + "_total"

		self._tick_num_array_day = []
		self._tick_num_array_night = []
		self._tick_num_array_total = []
		self._md_array = []

		self._file_nums = 0
		self._total_tick_num = 0


	def __del__(self):
		print "this is the over function " + self._config_file_day

		self._tick_num_array_day = sorted(self._tick_num_array_day)
		self._tick_num_array_night = sorted(self._tick_num_array_night)
		self._tick_num_array_total = sorted(self._tick_num_array_total)

		self._file_nums = len(self._tick_num_array_day)
		if self._file_nums !=0:
			avg = sum(self._tick_num_array_day)/self._file_nums
			print "the day avg is :"+ str(avg)
			medium = self._tick_num_array_day[self._file_nums/2]
			print "the day medium is : " + str(medium)
		print "the file num is : "+ str(self._file_nums)

		self._file_nums = len(self._tick_num_array_night)
		if self._file_nums !=0:
			avg = sum(self._tick_num_array_night)/self._file_nums
			print "the night avg is :"+ str(avg)
			medium = self._tick_num_array_night[self._file_nums/2]
			print "the night medium is : " + str(medium)
		print "the file num is : "+ str(self._file_nums)

		self._file_nums = len(self._tick_num_array_total)
		if self._file_nums !=0:
			avg = sum(self._tick_num_array_total)/self._file_nums
			print "the total avg is :"+ str(avg)
			medium = self._tick_num_array_total[self._file_nums/2]
			print "the total medium is : " + str(medium)
		print "the file num is : "+ str(self._file_nums)

		print "has write the config file"


	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		# tranfer the string to float
		self._md_array = md_array
		hour = md_array[0][3]
		hour_high = md_array[2]
		hour_low = md_array[3]
		if self._total_max_lastprice ==0 or self._total_max_lastprice < hour_high:
			self._total_max_lastprice = hour_high
		if self._total_min_lastprice ==0 or self._total_min_lastprice > hour_low:
			self._total_min_lastprice = hour_low
		if hour >=9 and hour <=15:
			# print "this is day"
			if self._day_min_lastprice ==0 or self._day_min_lastprice > hour_low:
				self._day_min_lastprice = hour_low
			if self._day_max_lastprice==0 or self._day_max_lastprice < hour_high:
				self._day_max_lastprice = hour_high
		else:
			# print "this is night"
			if self._night_min_lastprice ==0 or self._night_min_lastprice > hour_low:
				self._night_min_lastprice = hour_low
			if self._night_max_lastprice ==0 or self._night_max_lastprice < hour_high:
				self._night_max_lastprice = hour_high

	def get_tick_num(self):
		tick_num = (self._day_max_lastprice - self._day_min_lastprice)/self._tick
		if tick_num >=5:		
			self._tick_num_array_day.append(tick_num)
			self._day_max_lastprice =0
			self._day_min_lastprice = 0

		tick_num = (self._night_max_lastprice - self._night_min_lastprice)/self._tick
		if tick_num >=5:
			self._tick_num_array_night.append(tick_num)
			self._night_max_lastprice =0
			self._night_min_lastprice = 0

		tick_num = (self._total_max_lastprice - self._total_min_lastprice)/self._tick
		if tick_num >=5:
			self._tick_num_array_total.append(tick_num)
			self._total_max_lastprice =0
			self._total_min_lastprice = 0

def main():
	instrumentid = "v"
	path = "./data_wande/"+instrumentid+".xls"
	print path
	bt = GetRange(nameDict[instrumentid])
	bk = xlrd.open_workbook(path)
	shxrange = range(bk.nsheets)
	try:
		sh = bk.sheet_by_name("file")
	except:
		print "no sheet in %s named file" % path
	#获取行数
	nrows = sh.nrows
	#获取列数
	ncols = sh.ncols
	# print "nrows %d, ncols %d" % (nrows,ncols)
	row_list = []
	#获取各行数据
	for i in range(1,nrows):
		if sh.cell(i,0).ctype == 3: 
			date = xldate_as_tuple(sh.cell(i,0).value,0)
			row_data = sh.row_values(i)
			row_data[0] = date
			row_list.append(row_data)
	day = 0
	for row in row_list:
		row_day = row[0][2]
		if day !=0 and row_day != day:
			bt.get_tick_num()
		day = row_day
		bt.get_md_data(row)


if __name__=='__main__':
	main()