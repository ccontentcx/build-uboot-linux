import network
import socket
import time

# 创建AP接口
ap = network.WLAN(network.AP_IF)
ap.active(True)

# 设置SoftAP参数：SSID和密码
ssid = "RP2040-W-SoftAP"
password = "12345678"

ap.config(essid=ssid, password=password, )

print("SoftAP启动中...")
while not ap.active():
    time.sleep(1)

print("SoftAP已启动")
print("IP地址:", ap.ifconfig()[0])

# 创建一个简单的TCP服务器监听电脑连接
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
print('等待连接...')

while True:
    cl, addr = s.accept()
    print('客户端连接来自', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
        print(line)
    response = b"""\
HTTP/1.1 200 OK

Hello from RP2040-W SoftAP!
"""
    cl.send(response)
    cl.close()
