# -*- coding:utf8 -*-
import csv
import os
import cx_Oracle  

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
BIDPRICE1VOLUME = 23
ASKPRICE1 =24
ASKPRICE1VOLUME =25
TIME = 20
LONG =1
SHORT =0

# 这个是铅的
param_dict_pb = {"tick":5,"config_file":"pb"}
# 这个是螺纹钢的
param_dict_rb = {"tick":1,"config_file":"rb"}

# 这个是橡胶的
param_dic_ru = {"tick":5,"config_file":"ru"}

# 这个是锌的
param_dic_zn = {"tick":5,"config_file":"zn"}

param_dict_i = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":350}

param_dic_ni = {"tick":10,"config_file":"ni"}

param_dic_al = {"tick":5,"config_file":"al"}

param_dict_hc = {"tick":1,"config_file":"hc"}

param_dict_cu = {"tick":10,"config_file":"cu"}

param_dict_bu = {"tick":2,"config_file":"bu"}


param_dic_au = {"tick":0.05,"config_file":"au"}

param_dic_ag = {"tick":1,"config_file":"ag"}

param_dic_j = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":420}

param_dic_jm = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":60,"file":file,"config_file":430}

param_dic_pp = {"tick":1,"config_file":"pp"}

param_dic_v = {"tick":5,"config_file":"v"}

param_dic_y = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":460}

param_dic_p = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":470}

param_dic_c = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":480}

param_dic_a = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":490}

param_dic_m = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":500}

param_dic_jd = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":510}

nameDict = {
	"rb":{"param":param_dict_rb},
	"ru":{"param":param_dic_ru},
	"zn":{"param":param_dic_zn},
	"cu":{"param":param_dict_cu},
	"i":{"param":param_dict_i},
	"hc":{"param":param_dict_hc},
	"ni":{"param":param_dic_ni},
	"al":{"param":param_dic_al},
	"au":{"param":param_dic_au},
	"ag":{"param":param_dic_ag},
	"j1801":{"param":param_dic_j},
	"jm1801":{"param":param_dic_jm},
	"pp":{"param":param_dic_pp},
	"v":{"param":param_dic_v},
	"y1801":{"param":param_dic_y},
	"p1801":{"param":param_dic_p},
	"c1801":{"param":param_dic_c},
	"a1801":{"param":param_dic_a},
	"m1801":{"param":param_dic_m},
	"jd1801":{"param":param_dic_jd},
	"bu":{"param":param_dict_bu},
	"pb":{"param":param_dict_pb}
}

class GetRange(object):
	"""docstring for GetRange"""
	def __init__(self,param_dic):
		super(GetRange, self).__init__()

		self._max_lastprice = 0
		self._min_lastprice = 0

		self._tick = param_dic["tick"]
		self._config_file = param_dic["config_file"]

		self._tick_num_dict = {}

		self._file_nums = 0

		self._total_tick_num = 0


	def __del__(self):
		print "this is the over function " + self._config_file

		write_lines = []
		for item in self._tick_num_dict:
			if item>=0 and item <=4:
				continue
			self._total_tick_num += (item * self._tick_num_dict[item])
			self._file_nums += self._tick_num_dict[item]
			tmp_nums = self._tick_num_dict[item]
			tmp_dict = dict()
			tmp_dict["tick"] = item
			tmp_dict["nums"] = self._tick_num_dict[item]
			write_lines.append(tmp_dict)
		avg = self._total_tick_num/self._file_nums
		write_lines = sorted(write_lines, key=lambda tick_data : int(tick_data["tick"]))
		index = self._file_nums/2
		for x in xrange(0,len(write_lines)):
			index -= write_lines[x]["nums"]
			if index<=0:
				print "the mudium is : " + str(write_lines[x]["tick"])
				break
		print "the avg is :"+ str(avg)
		print "the file nums is :"+ str(self._file_nums)
		print "has write the config file"


	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		lastprice =  float(md_array[LASTPRICE])

		if self._max_lastprice == 0:
			self._max_lastprice = lastprice
		if self._min_lastprice ==0:
			self._min_lastprice = lastprice
		if lastprice > self._max_lastprice:
			self._max_lastprice = lastprice
		if lastprice < self._min_lastprice:
			self._min_lastprice = lastprice

	def get_tick_num(self):
		tick_num = (self._max_lastprice - self._min_lastprice)/self._tick
		tmp =tick_num
		if tmp in self._tick_num_dict:
			self._tick_num_dict[tmp] +=1
		else:
			self._tick_num_dict[tmp] =1
		self._max_lastprice =0
		self._min_lastprice = 0

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
	# for line in day:
	# 	ret.append(line)

	return ret




def main():
	total_path = "./data/"
	instrumentid = "ru"
	bt = GetRange(nameDict[instrumentid]["param"])
	print instrumentid
	for file in os.listdir(total_path):
		tmp =  os.path.join(total_path,file)
		if os.path.isdir(tmp):
			print tmp
			if instrumentid in tmp:
				for file_csv in os.listdir(tmp):
					# print file_csv
					file_csv = os.path.join(tmp,file_csv)
					f = open(file_csv,'rb')
					reader = csv.reader(f)
					tmpdata = []
					for row in reader:
						tmpdata.append(row)
					tmpdata = getSortedData(tmpdata)
					for row in tmpdata:
						bt.get_md_data(row)
						# tranfer the string to float
					bt.get_tick_num()
					f.close()
		else:
			print "this is file "


if __name__=='__main__':
	main()