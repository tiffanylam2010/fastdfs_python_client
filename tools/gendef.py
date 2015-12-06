# coding: utf8
import sys

HEADER = """# coding: utf8
#----此文件由tools/gendef.py自动生成---#

import ctypes

FDFS_MAX_META_NAME_LEN = 64+1
FDFS_MAX_META_VALUE_LEN = 256+1
class FDFSMetaData(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char*FDFS_MAX_META_NAME_LEN),
		("value", ctypes.c_char*FDFS_MAX_META_VALUE_LEN),
	]
	
IP_ADDRESS_SIZE = 16
class ConnectionInfo(ctypes.Structure):
	_fields_ = [
			("sock", ctypes.c_int),
			("port", ctypes.c_int),
			("ip_addr", ctypes.c_char*IP_ADDRESS_SIZE),
		]
	
class TrackerServerGroup(ctypes.Structure):
	_fields_ = [
			("server_count", ctypes.c_int),
			("server_index", ctypes.c_int),
			("servers", ctypes.POINTER(ConnectionInfo)*1)
		]

"""

# 定义c类型中对应的python的ctype类型和相关指针的类型;
# 不全, 只是添加了目前需要用到的几个类型
TYPE_DEFINE = {
	"bool": ("ctypes.c_bool", ""),
	"char": ("ctypes.c_char", "ctypes.c_char_p"),
	"int": ("ctypes.c_int", "ctypes.POINTER(ctypes.c_int)"),
	"int64_t": ("ctypes.c_int64", "ctypes.POINTER(ctypes.c_int64)"),
	"void": ("None", "ctypes.POINTER(ctypes.c_void_p)"),
	"ConnectionInfo": ("ConnectionInfo","ctypes.POINTER(ConnectionInfo)" ),
	"FDFSMetaData": ("FDFSMetaData","ctypes.POINTER(FDFSMetaData)" ),
	"TrackerServerGroup": ("TrackerServerGroup","ctypes.POINTER(TrackerServerGroup)" ),
}

def export_ctypes_define(libname, oristr):
	idx1 = oristr.find("(")
	idx2 = oristr.rfind(")")

	substr = oristr[:idx1].strip()
	return_type, function_name = substr.split()
	ispointer = 0
	if "*" in substr:
		ispointer = 1
		if function_name.strip().startswith("*"):
			function_name = function_name.strip()[1:]
			
	return_type = TYPE_DEFINE[return_type][ispointer]

	args_list = []
	s = oristr[idx1+1:idx2]
	s = s.replace("\\", " ")
	for item in s.split(","):
		item = item.strip()
		if not item: continue
		lst = item.split()
		argstype = lst[-2]
		ispointer = 0
		if "*" in item:
			ispointer = 1
		newtype = TYPE_DEFINE[argstype][ispointer]
		args_list.append( (newtype, item.strip()) )

	linelist= []
	if args_list:
		linelist.append( "%s.%s.argtypes = ["%(libname, function_name) )
		for args, oldargs,  in args_list:
			linelist.append( "\t\t%s, # %s"%(args, oldargs) )
		linelist.append( "\t]" )
	else:
		linelist.append( "%s.%s.argtypes = [ ]"%(libname, function_name) )
		
	linelist.append( "%s.%s.restype = %s"%(libname, function_name, return_type) )
	return "\n".join(linelist)

def gen_define(libname, input_filename, output_filename):
	fd = open(output_filename, "w")
	
	# 写入头部
	fd.write(HEADER)
	fd.write('%s = ctypes.cdll.LoadLibrary("libfdfsclient.so")\n'%libname)
	fd.write('\n\n')
	
	for text in open(input_filename).read().strip().split(";"):
		text = text.strip()
		if text:
			data = export_ctypes_define(libname, text)
			fd.write(data)
			fd.write("\n\n")
	
	fd.close()
	print "update file:", output_filename
		
if __name__ == '__main__':
	import os
	filedir = os.path.dirname(__file__)
	libname = "LIBFDFSCLIENT"
	input_filename = os.path.join(filedir, "c_function_define.txt")
	output_filename = os.path.abspath(os.path.join(filedir, "../fastdfs_c_define.py"))
	gen_define(libname, input_filename, output_filename)
			
			
