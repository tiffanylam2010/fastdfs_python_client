# coding: utf8
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

LIBFDFSCLIENT = ctypes.cdll.LoadLibrary("libfdfsclient.so")


LIBFDFSCLIENT.log_init.argtypes = [ ]
LIBFDFSCLIENT.log_init.restype = ctypes.c_int

LIBFDFSCLIENT.fdfs_client_init_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
		ctypes.c_char_p, # const char *conf_filename
	]
LIBFDFSCLIENT.fdfs_client_init_ex.restype = ctypes.c_int

LIBFDFSCLIENT.tracker_get_connection_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
	]
LIBFDFSCLIENT.tracker_get_connection_ex.restype = ctypes.POINTER(ConnectionInfo)

LIBFDFSCLIENT.fdfs_client_destroy_ex.argtypes = [
		ctypes.POINTER(TrackerServerGroup), # TrackerServerGroup *pTrackerGroup
	]
LIBFDFSCLIENT.fdfs_client_destroy_ex.restype = None

LIBFDFSCLIENT.tracker_connect_server_ex.argtypes = [
		ctypes.POINTER(ConnectionInfo), # ConnectionInfo *pTrackerServer
		ctypes.c_int, # const int connect_timeout
		ctypes.POINTER(ctypes.c_int), # int *err_no
	]
LIBFDFSCLIENT.tracker_connect_server_ex.restype = ctypes.POINTER(ConnectionInfo)

LIBFDFSCLIENT.storage_upload_by_filename1_ex.argtypes = [
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
LIBFDFSCLIENT.storage_upload_by_filename1_ex.restype = ctypes.c_int

LIBFDFSCLIENT.storage_do_upload_file1.argtypes = [
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
LIBFDFSCLIENT.storage_do_upload_file1.restype = ctypes.c_int

LIBFDFSCLIENT.storage_upload_slave_by_filename1.argtypes = [
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
LIBFDFSCLIENT.storage_upload_slave_by_filename1.restype = ctypes.c_int

LIBFDFSCLIENT.storage_upload_slave_by_filebuff1.argtypes = [
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
LIBFDFSCLIENT.storage_upload_slave_by_filebuff1.restype = ctypes.c_int

