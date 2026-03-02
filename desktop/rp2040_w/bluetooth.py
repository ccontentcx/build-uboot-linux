import bluetooth
import uasyncio as asyncio
import struct
import time
from micropython import const

# 定义 BLE 常量和 UUID
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# 构造 BLE GATT 服务
_UART_RX_CHAR = (
    _UART_RX_CHAR_UUID,
    bluetooth.FLAG_WRITE,  # 使用 FLAG_WRITE 兼容旧版固件
)
_UART_TX_CHAR = (
    _UART_TX_CHAR_UUID,
    bluetooth.FLAG_NOTIFY,
)
_UART_SERVICE = (
    _UART_SERVICE_UUID,
    (_UART_RX_CHAR, _UART_TX_CHAR),
)

# 广播数据
_ble_name = "PicoW_AsyncIO"
_adv_data = bytearray(b"\x02\x01\x06") + bytearray((len(_ble_name) + 1,)) + bytearray((0x09,)) + bytearray(_ble_name, "utf-8")

# 全局变量来管理连接和句柄
ble = bluetooth.BLE()
conn_handles = set()
tx_handle = None

# 处理 BLE 事件的回调函数
def ble_irq(event, data):
    global conn_handles
    global tx_handle
    if event == _IRQ_CENTRAL_CONNECT:
        conn_handle, _, _ = data
        conn_handles.add(conn_handle)
        print("设备已连接")
    elif event == _IRQ_CENTRAL_DISCONNECT:
        conn_handle, _, _ = data
        conn_handles.remove(conn_handle)
        print("设备已断开连接")
    elif event == _IRQ_GATTS_WRITE:
        conn_handle, value_handle = data
        value = ble.gatts_read(value_handle)
        # 在这里处理收到的数据
        print("收到数据:", value.decode())

# 广播任务，处理连接和断开
async def ble_advertise_task():
    global ble
    global tx_handle
    
    ble.active(True)
    ble.irq(ble_irq)
    
    ((rx_handle, tx_handle),) = ble.gatts_register_services((_UART_SERVICE,))
    
    while True:
        if not conn_handles:
            # 如果没有连接，开始广播
            ble.gap_advertise(100_000, adv_data=_adv_data)
            print("开始广播，设备名称:", _ble_name)
            await asyncio.sleep_ms(500) # 等待一段时间再检查
        await asyncio.sleep_ms(100)

# 数据发送任务
async def send_data_task():
    global ble
    global tx_handle
    counter = 0
    while True:
        if conn_handles and tx_handle:
            message = "Hello from Pico W! Count: {}".format(counter)
            print("发送数据:", message)
            for conn in conn_handles:
                try:
                    ble.gatts_notify(conn, tx_handle, message.encode())
                except Exception as e:
                    print("发送失败:", e)
            counter += 1
        await asyncio.sleep(2) # 暂停2秒

# 主任务
async def main():
    print("启动 asyncio BLE...")
    # 启动异步任务
    asyncio.create_task(ble_advertise_task())
    asyncio.create_task(send_data_task())
    
    # 可以在这里添加其他任务
    # asyncio.create_task(another_task())
    
    # 让事件循环一直运行
    while True:
        await asyncio.sleep(1)

# 启动事件循环
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序终止")
    finally:
        ble.active(False)
        print("BLE 已关闭")