# coding: utf8

import ctypes

libfdfs = ctypes.cdll.LoadLibrary("libfdfsclient.so")

IP_ADDRESS_SIZE = 16

STORAGE_PROTO_CMD_UPLOAD_FILE = 11
STORAGE_PROTO_CMD_DELETE_FILE = 12
STORAGE_PROTO_CMD_SET_METADATA = 13
STORAGE_PROTO_CMD_DOWNLOAD_FILE = 14
STORAGE_PROTO_CMD_GET_METADATA = 15
STORAGE_PROTO_CMD_UPLOAD_SLAVE_FILE = 21

FDFS_UPLOAD_BY_BUFF = 1
FDFS_UPLOAD_BY_FILE = 2

FDFS_MAX_META_NAME_LEN = 64+1
FDFS_MAX_META_VALUE_LEN = 256+1

class FDFSMetaData(ctypes.Structure):
	_fields_ = [
		("name", ctypes.c_char*FDFS_MAX_META_NAME_LEN),
		("value", ctypes.c_char*FDFS_MAX_META_VALUE_LEN),
	]

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

libfdfs.log_init.argtypes = [ ]
libfdfs.log_init.restype = ctypes.c_int

libfdfs.fdfs_client_init_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
		ctypes.c_char_p, # const char *conf_filename
	]
libfdfs.fdfs_client_init_ex.restype = ctypes.c_int

libfdfs.tracker_get_connection_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
	]
libfdfs.tracker_get_connection_ex.restype = ctypes.POINTER(ConnectionInfo)

libfdfs.fdfs_client_destroy_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
	]
libfdfs.fdfs_client_destroy_ex.restype = None

libfdfs.tracker_connect_server_ex.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.c_int, # const int connect_timeout
		ctypes.POINTER(ctypes.c_int), # int *err_no
	]
libfdfs.tracker_connect_server_ex.restype = ctypes.POINTER(ConnectionInfo)

libfdfs.storage_upload_by_filename1_ex.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pStorageServer
		ctypes.c_int, # const int store_path_index
		ctypes.c_char, # const char cmd
		ctypes.c_char_p, # const char *local_filename
		ctypes.c_char_p, # const char *file_ext_name
		ctypes.POINTER(FDFSMetaData), # const FDFSMetaData *meta_list
		ctypes.c_int, # const int meta_count
		ctypes.c_char_p, # const char *group_name
		ctypes.c_char_p, # char *file_id
	]
libfdfs.storage_upload_by_filename1_ex.restype = ctypes.c_int

libfdfs.storage_do_upload_file1.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pStorageServer
		ctypes.c_int, # const int store_path_index
		ctypes.c_char, # const char cmd
		ctypes.c_int, # const int upload_type
		ctypes.c_char_p, # const char *file_buff
		ctypes.POINTER(ctypes.c_void_p), # void *arg
		ctypes.c_int64, # const int64_t file_size
		ctypes.c_char_p, # const char *file_ext_name
		ctypes.POINTER(FDFSMetaData), # const FDFSMetaData *meta_list
		ctypes.c_int, # const int meta_count
		ctypes.c_char_p, # const char *group_name
		ctypes.c_char_p, # char *file_id
	]
libfdfs.storage_do_upload_file1.restype = ctypes.c_int

libfdfs.storage_upload_slave_by_filename1.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pStorageServer
		ctypes.c_char_p, # const char *local_filename
		ctypes.c_char_p, # const char *master_file_id
		ctypes.c_char_p, # const char *prefix_name
		ctypes.c_char_p, # const char *file_ext_name
		ctypes.POINTER(FDFSMetaData), # const FDFSMetaData *meta_list
		ctypes.c_int, # const int meta_count
		ctypes.c_char_p, # char *file_id
	]
libfdfs.storage_upload_slave_by_filename1.restype = ctypes.c_int

libfdfs.storage_upload_slave_by_filebuff1.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pStorageServer
		ctypes.c_char_p, # const char *file_buff
		ctypes.c_int64, # const int64_t file_size
		ctypes.c_char_p, # const char *master_file_id
		ctypes.c_char_p, # const char *prefix_name
		ctypes.c_char_p, # const char *file_ext_name
		ctypes.POINTER(FDFSMetaData), # const FDFSMetaData *meta_list
		ctypes.c_int, # const int meta_count
		ctypes.c_char_p, # char *file_id
	]
libfdfs.storage_upload_slave_by_filebuff1.restype = ctypes.c_int


class FastDFSClient(object):
	def __init__(self, client_conf_file):
		self._group = TrackerServerGroup()
		self.p_group = ctypes.pointer(self._group)
		libfdfs.log_init()
		errno = libfdfs.fdfs_client_init_ex(self.p_group, client_conf_file) 
		if errno != 0:
			raise Exception("init failed errno:%d"%errno)
	
	def _get_tracker(self):
		p_tracker = libfdfs.tracker_get_connection_ex(self.p_group)
		if bool(p_tracker):
			# 如果tracker_get_connection_ex失败返回的是空指针
			# 通过bool可以判断p_tracker是否空指针
			return p_tracker
		else:
			return None
	
	def _pack_meta(self, meta_dict):
		p_meta = None
		meta_count = 0

		if meta_dict:
			meta_count = len(meta_dict)
			p_meta = (FDFSMetaData*meta_count)()
			for i,key in enumerate(meta_dict.keys()):
				value = meta_dict[key]
				p_meta[i].name = key
				p_meta[i].value = value

		return p_meta, meta_count
		
	def destroy(self):
		libfdfs.fdfs_client_destroy_ex(self.p_group)
		
	def _get_file_ext_name(self, filename):
		file_ext_name = ""
		if "." in filename:
			file_ext_name = filename.split(".")[-1]
		return file_ext_name
		
	def _call_upload(self, upload_type, argv, meta_dict=None):
		p_tracker = self._get_tracker()
		if not p_tracker:
			return False, "connect to tracker failed"
			
		p_meta, meta_count = self._pack_meta(meta_dict)
		file_id = ctypes.create_string_buffer(256)
		if upload_type == 'master_buffer':
			content = argv['content']
			file_ext_name = argv['file_ext_name']
			errno = libfdfs.storage_do_upload_file1(
					p_tracker, # ConnectionInfo *pTrackerServer
					None, # ConnectionInfo *pStorageServer
					0, # const int store_path_index
					ctypes.c_char(chr(STORAGE_PROTO_CMD_UPLOAD_FILE)), # const char cmd
					FDFS_UPLOAD_BY_BUFF, # const int upload_type
					content, # const char *file_buff
					None, # void *arg
					len(content), # const int64_t file_size
					file_ext_name, # const char *file_ext_name
					p_meta, # const FDFSMetaData *meta_list
					meta_count, # const int meta_count
					None, # const char *group_name
					file_id, # char *file_id
				)
		elif upload_type == 'master_file':
			file_path = argv['file_path']
			file_ext_name = self._get_file_ext_name(file_path)
			errno = libfdfs.storage_upload_by_filename1_ex(
					p_tracker,# ConnectionInfo *pTrackerServer
					None,  # ConnectionInfo *pStorageServer
					0, # const int store_path_index
					ctypes.c_char(chr(STORAGE_PROTO_CMD_UPLOAD_FILE)),# const char cmd
					file_path, # const char *local_filename
					file_ext_name, # const char *file_ext_name
					p_meta, # const FDFSMetaData *meta_list
					meta_count, # const int meta_count
					None,# const char *group_name
					file_id # char *file_id
				)
		elif upload_type == 'slave_buffer':
			content = argv['content']
			prefix_name = argv['prefix_name']
			master_file_name = argv['master_file_name']
			file_ext_name = self._get_file_ext_name(master_file_name)
			errno = libfdfs.storage_upload_slave_by_filebuff1(
					p_tracker, # ConnectionInfo *pTrackerServer
					None, # ConnectionInfo *pStorageServer
					content, # const char *file_buff
					len(content), # const int64_t file_size
					master_file_name, # const char *master_file_id
					prefix_name, # const char *prefix_name
					file_ext_name, # const char *file_ext_name
					p_meta, # const FDFSMetaData *meta_list
					meta_count,# const int meta_count
					file_id# char *file_id
				)
		elif upload_type == 'slave_file':
			file_path = argv['file_path']
			prefix_name = argv['prefix_name']
			master_file_name = argv['master_file_name']
			file_ext_name = self._get_file_ext_name(master_file_name)
			errno = libfdfs.storage_upload_slave_by_filename1(
					p_tracker,# ConnectionInfo *pTrackerServer
					None,  # ConnectionInfo *pStorageServer
					file_path, # const char *local_filename
					master_file_name, # const char *master_file_id
					prefix_name, # const char *prefix_name
					file_ext_name, # const char *file_ext_name
					p_meta, # const FDFSMetaData *meta_list
					meta_count, # const int meta_count
					file_id # char *file_id
				)
		else:
			raise Exception("unknown upload_type:%r"%upload_type)
			
		if errno == 0:
			return True, file_id.value
		else:
			return False, os.strerror(errno)

	def upload_by_buffer(self, content, file_ext_name, meta_dict=None):
		argv = {'content': content, 'file_ext_name': file_ext_name}
		return self._call_upload(upload_type="master_buffer", 
					argv=argv, meta_dict=meta_dict)
	
	def upload_by_file(self, file_path, meta_dict=None):
		argv = {'file_path': file_path}
		return self._call_upload(upload_type="master_file", 
					argv=argv, meta_dict=meta_dict)

	def upload_slave_by_buffer(self, content, prefix_name, master_file_name, meta_dict=None):
		argv = {'content': content, 
				'prefix_name': prefix_name, 
				'master_file_name': master_file_name,
				}
		return self._call_upload(upload_type="slave_buffer", 
					argv=argv, meta_dict=meta_dict)

	def upload_slave_by_file(self, file_path, prefix_name, master_file_name, meta_dict=None):
		argv = {'file_path': file_path, 
				'prefix_name': prefix_name, 
				'master_file_name': master_file_name,
				}
		return self._call_upload(upload_type="slave_file", 
					argv=argv, meta_dict=meta_dict)

	
if __name__ == '__main__':
	obj = FastDFSClient("./client.conf")
	meta_dict = {"A":"xx", "B": "yy"}
	ok, filename = obj.upload_by_buffer("aaaaaabbbb", "txt", meta_dict)
	print "upload_by_buffer:", ok, filename
	ok, filename = obj.upload_slave_by_buffer("slave_abc", "-small", filename, meta_dict)
	print "upload_slave_by_buffer:", ok, filename
	
	ok, filename = obj.upload_by_file("./client.conf", meta_dict)
	print "upload_by_file:", ok, filename
	ok, filename = obj.upload_slave_by_file("./client.conf", "-big", filename, meta_dict)
	print "upload_slave_by_file:", ok, filename
	
	obj.destroy()
	
