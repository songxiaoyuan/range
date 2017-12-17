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


	def __del__(self):
		print "this is the over function " + self._config_file

		config_file = "./range_config/"+self._config_file+'.csv'
		file = open(config_file,"w")
		write_lines = []
		for item in self._tick_num_dict:
			tmp = str(5*item) + " - " + str(5*item + 4)
			line = tmp + " : "+ str(self._tick_num_dict[item]) + '\n'
			write_lines.append(line)
			# print int(line.split(":")[0].split('-')[0])
		write_lines = sorted(write_lines, key=lambda tick_data : int(tick_data.split(":")[0].split('-')[0]))
		file.writelines(write_lines)
		file.close()
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
		tmp = int(tick_num/5)
		if tmp in self._tick_num_dict:
			self._tick_num_dict[tmp] +=1
		else:
			self._tick_num_dict[tmp] =1
		self._max_lastprice =0
		self._min_lastprice = 0

def clean_night_data(data):
	ret = []
	amBegin = 9*3600
	pmEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[0].split(":")
		# print timeLine
		# tick = line[21]
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime>=amBegin and nowTime <=pmEnd:
			ret.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	return ret



def main():
	total_path = "./data/"
	instrumentid = "hc"
	bt = GetRange(nameDict[instrumentid]["param"])
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
					for row in reader:
						bt.get_md_data(row)
						# tranfer the string to float
					bt.get_tick_num()
					f.close()
		else:
			print "this is file "
	# data = data10
	# # instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	# instrumentid_array = ["rb1801"]
	# for instrumentid in instrumentid_array:
	# 	# instrumentid = "pb1711"
	# 	bt = GetRange(nameDict[instrumentid]["param"])
	# 	for item in data:
	# 		filename = instrumentid+ "_"+str(item)
	# 		path = "../data/"+filename+".csv"
	# 		# path = "../data/"+filename
	# 		# read_data_from_csv(path)
	# 		f = open(path,'rb')
	# 		print "the instrument id is: "+filename
	# 		reader = csv.reader(f)
	# 		for row in reader:
	# 			bt.get_md_data(row)
	# 			# tranfer the string to float
	# 		bt.get_tick_num()
	# 		f.close()


if __name__=='__main__':
	main()