import uasyncio as asyncio
import time
from machine import Pin, I2C
# 确保 mpu6050.py 文件已经上传
from MPU6050_MPU6050_lib import MPU6050

# I2C 总线初始化
# 根据你的连接选择 I2C 控制器 (0 或 1) 和引脚。
# 以下示例使用 I2C0, SDA在GP0, SCL在GP1。
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

# 初始化 MPU6050 对象
# 默认的I2C地址是 0x68
mpu = MPU6050(i2c)

# 异步任务: 读取和打印传感器数据
async def read_mpu6050():
    print("MPU6050 传感器数据读取任务启动...")
    while True:
        try:
            # 读取数据
            accel = mpu.accel
            gyro = mpu.gyro
            temp = mpu.temperature

            # 打印数据
            print(f"加速度计: X:{accel.x:.2f}, Y:{accel.y:.2f}, Z:{accel.z:.2f}")
            print(f"陀螺仪:   X:{gyro.x:.2f}, Y:{gyro.y:.2f}, Z:{gyro.z:.2f}")
            print(f"温度:     {temp:.2f} ℃")
            print("-" * 30)

        except OSError as e:
            print(f"I2C通信错误: {e}")
            # 如果出现I2C错误，稍作等待后尝试重新初始化
            await asyncio.sleep(1)
            # 在某些情况下，可能需要重新创建MPU6050对象，但通常只需等待
            continue

        # 异步等待，让出CPU给其他任务
        await asyncio.sleep(1)

# 异步任务: 模拟另一个后台任务
async def another_task():
    count = 0
    while True:
        print(f"另一个任务正在运行... 计数: {count}")
        count += 1
        # 异步等待，让出CPU
        await asyncio.sleep(3) # 间隔长一些，方便观察

# 主异步函数
async def main():
    # 创建并运行两个异步任务
    asyncio.create_task(read_mpu6050())
    asyncio.create_task(another_task())

    # 让主循环持续运行，直到所有任务完成
    # 在这个例子中，任务都是无限循环，所以程序会一直运行下去
    while True:
        await asyncio.sleep(100)

# 启动 asyncio 事件循环
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已停止。")