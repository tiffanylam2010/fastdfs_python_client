FastDFS Python Client (Ctypes Version)
======
用ctypes调用[FastDFS](https://github.com/happyfish100/fastdfs.git)原版client的c接口, 并把c接口依赖的流程组合起来.

##依赖:
* 依赖FastDFS原版的client编译出来的libfdfsclient.so
* 目前在debian7+python2.7下测试通过
	
##功能:
* 由于FastDFS一般是上传使用API,下载用http, 所以目前只提供了以下接口:

		upload_by_buffer
		upload_by_file
		upload_slave_by_buffer
		upload_slave_by_file

* 如果需要,可以继续添加接口, 方法如下:

		第一步: 在tools/c_function_define.txt中添加需要的接口中c中的定义
		第二步: 运行tools/gendef.py, 这步是根据定义更新 fastdfs_c_define.py
		第三步: 在fastdfs_client.py的FastDFSClient类中添加相关的函数调用
	
## 用法:
```python
import fastdfs_client
# 参数 client_conf_file: 是fastdfs原始的客户端配置文件;
# 也可以是简化版: 每行一个tracker server的配置:
# tracker_server=192.168.183.129:22122
client = fastdfs_client.FastDFSClient("./tools/client.conf")

# upload都支持meta的设置,默认不设置;
# 注意: meta的设置在存储中会多一个文件
# upload by buffer:
ok, filename = client.upload_by_buffer("hello,master", "txt")
print ok, filename
# >>> True group1/M00/00/00/wKi3gVZjn8-ABy0-AAAAIZTVx1k695.txt
ok, slave_filename = client.upload_slave_by_buffer("hello,slave", "-small", filename)
print ok, slave_filename
# >>> True group1/M00/00/00/wKi3gVZjn8-ABy0-AAAAIZTVx1k695-small.txt

# or upload by file:
ok, filename = client.upload_by_file("./tools/client.conf")
print ok, filename
# >>> True group1/M00/00/00/wKi3gVZjoAWAf9ECAAABI9DxThI87.conf
ok, slave_filename = client.upload_slave_by_file("./tools/client.conf", "-big", filename)
print ok, slave_filename
#>>> True group1/M00/00/00/wKi3gVZjoAWAf9ECAAABI9DxThI87-big.conf

# at last:
client.destroy()
```

