# coding: utf8
import sys

# lines = []
# while True:
	# try:
		# s = raw_input("")
		# lines.append(s)
	# except:
		# break
# text = "\n".join(lines)
# print text

s = """
int storage_do_upload_file1(ConnectionInfo *pTrackerServer, \
		ConnectionInfo *pStorageServer, const int store_path_index, \
		const char cmd, const int upload_type, \
		const char *file_buff, void *arg, const int64_t file_size, \
		const char *file_ext_name, const FDFSMetaData *meta_list, \
		const int meta_count, const char *group_name, char *file_id);
"""

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

	if args_list:
		print "%s.%s.argtypes = ["%(libname, function_name)
		for args, oldargs,  in args_list:
			print "\t\t%s, # %s"%(args, oldargs)
		print "\t]"
	else:
		print "%s.%s.argtypes = [ ]"%(libname, function_name)
		
	print "%s.%s.restype = %s"%(libname, function_name, return_type)


		
if __name__ == '__main__':
	libname = sys.argv[1]
	filename = sys.argv[2]
	for text in open(filename).read().strip().split(";"):
		text = text.strip()
		if text:
			export_ctypes_define(libname, text)
			print
