# mqtt_module.py
import asyncio
import random
import paho.mqtt.client as mqtt
import cbor2
import time

broker = "broker.hivemq.com"
port = 1883
topic = "test/topic_rp2040_w"
keepalive = 60

class MQTTClient:
    def __init__(self, client_id=None,):
        if client_id is None:
            client_id = f'device-{random.randint(1000,9999)}'

        self.client_id = client_id
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        print(f"[{self.client_id}] Connected with result code {rc}")
        if rc == 0:
            self.connected = True
            client.subscribe(topic)
            print(f"[{self.client_id}] Subscribed to topic {topic}")

    def on_disconnect(self, client, userdata, rc):
        print(f"[{self.client_id}] Disconnected with result code {rc}")
        self.connected = False

    def on_message(self, client, userdata, msg):
        try:
            data = cbor2.loads(msg.payload)
            print(f"[{self.client_id}] Received: {data}")
        except Exception as e:
            print(f"[{self.client_id}] CBOR decode error: {e}")

    def connect_and_loop(self):
        try:
          self.client.connect(broker, port, keepalive)
          self.client.loop_start()
        except Exception as e:
            print(f"[{self.client_id}] MQTT connect error: {e}")

    def publish_cbor(self, data_dict):
        if not self.connected:
            print("⚠️ MQTT not connected, can't publish.")
            return
        encoded = cbor2.dumps(data_dict)
        self.client.publish(topic, encoded, qos=1)
        print(f"[{self.client_id}] Published: {data_dict}")

# 用于测试时运行：
if __name__ == "__main__":
    import time
    mqttc = MQTTClient()
    mqttc.connect_and_loop()
    #time.sleep(2)  # 等连接上

    count = 0
    while True:
        mqttc.publish_cbor({"test": count,"client_id": mqttc.client_id})
        count+= 1
        time.sleep(20)
