import socket
import PIL.Image as PIm
import io
import time


def send_message(message: str, ip_: str, port_: int= 3048):
    if not message:
        return
    tcpClient2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    host = socket.gethostname()
    port = port_
    # addr = ('127.0.0.1', port)
    addr = (ip_, port)
    tcpClient2.connect(addr)  # 连接服务，指定主机和端口号

    label = message
    data = label.encode('utf-8')
    tcpClient2.send(data)
    print('send '+message+' to '+ip_+':'+str(port_)+' successfully!')
    tcpClient2.close()
    # while True:
    #     # label = open('E:/Users/19418/Desktop/label.txt', 'r')
    #     label = message
    #     # data = label.read().encode('utf-8')  # 报文数据，bytes类型
    #     data = label.encode('utf-8')  # 报文数据，bytes类型
    #     tcpClient.send(data)  # 发送数据给服务端
    #     # msg = tcpClient.recv(1024)  # 接收来自服务端的数据，小于1024字节
    #     # print(msg.decode('utf-8'))
    #     time.sleep(1)
    # tcpClient.close()


