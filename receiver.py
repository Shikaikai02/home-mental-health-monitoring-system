import socket
import PIL.Image
import io

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象，走tcp通道
host = socket.gethostname()  # 获取本地主机名
port = 3048  # 端口号
addr = ('192.168.137.117', port)
tcpServer.bind(addr)  # 绑定地址
tcpServer.listen(5)  # 设置最大连接数，超过后排队
conn, addr = tcpServer.accept()  # 建立客户端连接
print(conn)

while True:
    # print(233)
    # conn, addr = tcpServer.accept()  # 建立客户端连接
    # print(conn)
    data = conn.recv(100000)  # 接收来自客户端的数据，小于1024字节
    # print('received: ',end='')

    label = data.decode('utf-8')

    print('received: ', end='')
    print(label, end='')
    # print(type(label))
    wrl = open('/home/group6/label.txt', 'w')
    wrl.write(label)
    aaaa = open('/home/group6/label.txt', 'r')
    print(',', aaaa.read())
conn.close()  # 关闭连接

