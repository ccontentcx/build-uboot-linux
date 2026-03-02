from machine import Pin, PWM
import time

# Pico W 的板载 LED 连接在 GPIO 25
pwm = PWM(Pin(25))

# 设置 PWM 信号的频率
pwm.freq(1000)

# 定义一个函数，用于平滑地改变 LED 亮度
def fade_led():
    # 渐亮循环，占空比从 0 增加到 65535
    for duty in range(0, 65535, 100):
        pwm.duty_u16(duty)
        time.sleep_us(1000)

    # 渐灭循环，占空比从 65535 减少到 0
    for duty in range(65535, 0, -100):
        pwm.duty_u16(duty)
        time.sleep_us(1000)

# 主循环
while True:
    fade_led()
    time.sleep(1)