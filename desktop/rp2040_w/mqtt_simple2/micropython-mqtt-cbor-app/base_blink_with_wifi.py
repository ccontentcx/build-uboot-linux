import uasyncio as asyncio
from machine import Pin
import network
import gc

led = Pin("LED", Pin.OUT)

async def blink_led():
    while True:
        led.toggle()
        await asyncio.sleep(1)

async def wifi_task():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('辉煌', 'chenwen6666chao')
    try:
        while not wlan.isconnected():
            print("Waiting for connection...")
            await asyncio.sleep(0.5)
        print("Connected:", wlan.ifconfig())
    except Exception as e:
        print("WiFi连接失败:", e)

#async def main():
#    await asyncio.gather(blink_led(), wifi_task())
#asyncio.run(main())
