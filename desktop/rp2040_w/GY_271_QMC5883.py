from machine import Pin, I2C
import asyncio
import time
import math

# 配置 I2C
# 这里的 Pin(4) 和 Pin(5) 是一个示例，请根据你的开发板连接情况进行修改
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=100000)

QMC5883L_ADDR = 0x0D

# 模块配置
REG_CONFIG_1 = 0x09
REG_CONFIG_2 = 0x0A
REG_MODE_CONTINUOUS = 0x01
REG_ODR_100Hz = 0x0C
REG_RANGE_2G = 0x00
REG_OSR_512 = 0x30

async def setup_sensor():
    """异步初始化和配置传感器"""
    print("I2C 设备扫描结果:", i2c.scan())
    if QMC5883L_ADDR not in i2c.scan():
        print("未找到 GY-271 模块！请检查接线。")
        return False
    else:
        print("GY-271 模块已找到。")
    
    config_1 = REG_MODE_CONTINUOUS | REG_ODR_100Hz | REG_RANGE_2G | REG_OSR_512
    try:
        # 使用非阻塞的方式写入 I2C
        i2c.writeto_mem(QMC5883L_ADDR, REG_CONFIG_1, bytes([config_1]))
        await asyncio.sleep_ms(10) # 模拟异步等待
        i2c.writeto_mem(QMC5883L_ADDR, 0x0B, b'\x01')
        await asyncio.sleep_ms(100)
    except OSError as e:
        print(f"I2C 写入错误: {e}")
        return False
    
    return True

async def read_raw_data():
    """异步读取原始磁力计数据"""
    try:
        data = i2c.readfrom_mem(QMC5883L_ADDR, 0x00, 6)
        
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        
        # 将16位补码数据转换为有符号数
        if x > 32767:
            x -= 65536
        if y > 32767:
            y -= 65536
        if z > 32767:
            z -= 65536
            
        return x, y, z
    except OSError as e:
        print(f"I2C 读取错误: {e}")
        return None, None, None

def calculate_heading(x, y):
    """计算航向角"""
    heading = math.degrees(math.atan2(y, x))
    if heading < 0:
        heading += 360
    return heading

async def main_loop():
    """主异步任务循环"""
    if not await setup_sensor():
        return
        
    while True:
        x, y, z = await read_raw_data()
        
        if x is not None and y is not None:
            heading = calculate_heading(x, y)
            print(f"X: {x}, Y: {y}, Z: {z}, 航向角: {heading:.2f} 度")
        
        # 将控制权让给其他任务，每隔10毫秒运行一次
        await asyncio.sleep_ms(10)

# 启动异步事件循环
if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("程序终止。")