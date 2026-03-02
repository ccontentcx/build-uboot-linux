from machine import Pin, I2C
import time
import uasyncio as asyncio

# --- I2C 配置 ---
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# --- BMP280 I2C 地址和寄存器 ---
I2C_ADDR = 0x76
REG_ID = 0xD0
REG_CTRL_MEAS = 0xF4
REG_CONFIG = 0xF5
REG_PRESS_MSB = 0xF7
REG_CALIB = 0x88

# --- 全局变量 ---
cal_T = []
cal_P = []
t_fine = 0

# --- 辅助函数 (保持不变) ---
def read_register(reg_addr, num_bytes):
    return i2c.readfrom_mem(I2C_ADDR, reg_addr, num_bytes)

def write_register(reg_addr, value):
    i2c.writeto_mem(I2C_ADDR, reg_addr, bytes([value]))

def get_word(data):
    return data[0] + (data[1] << 8)

def get_uword(data):
    val = data[0] + (data[1] << 8)
    if val & 0x8000:
        val -= 0x10000
    return val

# --- 核心函数 (保持不变) ---
def read_calibration_data():
    global cal_T, cal_P
    data = read_register(REG_CALIB, 24)
    cal_T.append(get_word(data[0:2]))
    cal_T.append(get_uword(data[2:4]))
    cal_T.append(get_uword(data[4:6]))
    cal_P.append(get_word(data[6:8]))
    cal_P.append(get_uword(data[8:10]))
    cal_P.append(get_uword(data[10:12]))
    cal_P.append(get_uword(data[12:14]))
    cal_P.append(get_uword(data[14:16]))
    cal_P.append(get_uword(data[16:18]))
    cal_P.append(get_uword(data[18:20]))
    cal_P.append(get_uword(data[20:22]))
    cal_P.append(get_uword(data[22:24]))
    print("校准数据读取完成。")

def get_compensated_temperature(adc_T):
    global t_fine
    var1 = ((adc_T / 16384.0) - (cal_T[0] / 1024.0)) * cal_T[1]
    var2 = (((adc_T / 131072.0) - (cal_T[0] / 8192.0)) * ((adc_T / 131072.0) - (cal_T[0] / 8192.0))) * cal_T[2]
    t_fine = var1 + var2
    temp = t_fine / 5120.0
    return temp

def get_compensated_pressure(adc_P):
    var1 = (t_fine / 2.0) - 64000.0
    var2 = var1 * var1 * (cal_P[5] / 131072.0)
    var2 = var2 + (var1 * cal_P[4] * 2.0)
    var2 = (var2 + (cal_P[3] * 65536.0))
    var1 = (((cal_P[2] * var1 * var1) / 524288.0) + (cal_P[1] * var1)) / 524288.0
    var1 = (1.0 + (var1 / 32768.0)) * cal_P[0]
    if var1 == 0:
        return 0
    p = 1048576.0 - adc_P
    p = ((p - (var2 / 4096.0)) * 6250.0) / var1
    var1 = (cal_P[8] * p * p) / 2147483648.0
    var2 = (p * cal_P[7]) / 32768.0
    p = p + (var1 + var2 + cal_P[6]) / 16.0
    return p

# --- 异步任务 ---
async def read_loop(interval=1):
    """异步读取 BMP280 数据的协程"""
    while True:
        # 读取原始数据
        raw_p = read_register(REG_PRESS_MSB, 3)
        raw_t = read_register(0xFA, 3)
        
        # 组合24位数据
        adc_P = (raw_p[0] << 12) + (raw_p[1] << 4) + (raw_p[2] >> 4)
        adc_T = (raw_t[0] << 12) + (raw_t[1] << 4) + (raw_t[2] >> 4)
        
        # 计算温度和气压
        temperature = get_compensated_temperature(adc_T)
        pressure = get_compensated_pressure(adc_P)
        
        # 打印结果
        print("---------------------------------")
        print("- -> 温度: {:.2f} °C, 气压: {:.2f} hPa".format(
            temperature, pressure / 100))
        print("---------------------------------")
        
        # 异步等待，让出CPU给其他任务
        await asyncio.sleep(interval)

async def main():
    """主协程，用于启动其他异步任务"""
    
    # 1. 检查芯片ID
    chip_id = read_register(REG_ID, 1)
    if chip_id[0] != 0x58:
        print("未找到 BMP280 芯片，ID:", hex(chip_id[0]))
        return  # 如果没有找到芯片，退出主程序
    else:
        print("BMP280 芯片ID:", hex(chip_id[0]))
    
    # 2. 读取校准数据
    read_calibration_data()
    
    # 3. 配置传感器
    write_register(REG_CTRL_MEAS, 0x2F) 
    write_register(REG_CONFIG, 0xA0)
    
    await asyncio.sleep_ms(2000) # 等待传感器配置完成，这里用异步等待
    
    # 启动传感器读取任务
    asyncio.create_task(read_loop(interval=0.5)) # 每2秒读取一次
    
    # 这里的 `main` 协程可以继续做其他事，比如启动另一个任务
    while True:
#        print("主程序正在运行...")
        await asyncio.sleep(1) # 每5秒打印一次
        
# 启动 asyncio
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()  # 确保事件循环被清理