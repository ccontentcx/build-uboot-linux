import uasyncio as asyncio
from machine import Pin
import network
import gc
#import mip
#mip.install("aioble")
import aioble
import bluetooth
print(bluetooth)

led = Pin("LED", Pin.OUT)

# 蓝牙设备名字
DEVICE_NAME = "PicoW_BLE_Demo"



async def bluetooth_f():
    # 创建广播（advertisement）
    aioble.advertise(
        interval_us=500000,  # 广播间隔（500ms）
        name=DEVICE_NAME     # 广播名字
    )
    print("开始广播，打开手机蓝牙搜索：", DEVICE_NAME)
    while True:
        await asyncio.sleep(1)

async def blink_led():
    while True:
        led.toggle()
        await asyncio.sleep(1)

async def wifi_task():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('辉煌', 'chenwen6666chao')
    
    mac_bytes = wlan.config('mac')
    mac_address = ":".join(f"{b:02x}" for b in mac_bytes)
    try:
        while not wlan.isconnected():
            print("Waiting for connection...")
            await asyncio.sleep(0.5)
        print("Connected:", wlan.ifconfig())
        print(f"MAC 地址:       {mac_address}")
    except Exception as e:
        print("WiFi连接失败:", e)

async def main():
   await asyncio.gather(blink_led(), wifi_task(),bluetooth_f())
asyncio.run(main())
