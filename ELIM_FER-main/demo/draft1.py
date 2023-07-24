import socket
import PIL.Image as PIm
import io
import time

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
host = socket.gethostname()
port = 4049
# addr = ('127.0.0.1', port)
addr = ('172.25.109.153', port)
tcpClient.connect(addr)  # 连接服务，指定主机和端口号
while True:
    label = open('./label_.txt', 'r')
    #label = 'this is a message'
    data = label.read().encode('utf-8')  # 报文数据，bytes类型
    #data = label.encode('utf-8')  # 报文数据，bytes类型
    tcpClient.send(data)  # 发送数据给服务端
    # msg = tcpClient.recv(1024)  # 接收来自服务端的数据，小于1024字节
    # print(msg.decode('utf-8'))
    time.sleep(1)
tcpClient.close()

