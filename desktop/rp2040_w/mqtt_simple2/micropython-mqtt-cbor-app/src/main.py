import network
import time
import machine
from simple2 import MQTTClient
import cbor

# WiFi配置
SSID = '辉煌'
PASSWORD = 'chenwen6666chao'

# MQTT配置
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = b"test/topic_rp2040_w"
CLIENT_ID = b"rp2040w_" + str(machine.unique_id())

# WiFi连接函数
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("连接WiFi中...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("连接成功，IP:", wlan.ifconfig())

# MQTT消息回调
def mqtt_callback(topic, msg):
    try:
        data = cbor.loads(msg)
        print("收到CBOR消息：", data)
    except Exception as e:
        print("解析CBOR失败：", e)

# 发布函数（供外部调用）
def publish_message(client, data):
    try:
        payload = cbor.dumps(data)
        client.publish(TOPIC, payload)
        print("已发布：", data)
    except Exception as e:
        print("发布失败：", e)

# 主程序入口
def main():
    connect_wifi()
    print("连接MQTT...")
    client = MQTTClient(client_id=CLIENT_ID,
                        server=BROKER,
                        port=PORT,
                        keepalive=30)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(TOPIC)
    print("MQTT连接成功，已订阅", TOPIC)

    # 定时发布
    last_pub = time.time()
    counter = 0

    try:
        while True:
            client.check_msg()  # 检查是否有新消息（非阻塞）

            if time.time() - last_pub > 5:
                counter += 1
                msg = {"from": CLIENT_ID.decode(), "count": counter}
                publish_message(client, msg)
                last_pub = time.time()

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("断开MQTT")
        client.disconnect()

main()
