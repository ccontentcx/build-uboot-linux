from machine import Pin, SPI
import framebuf
import uasyncio as asyncio
import time
import gc
from machine import lightsleep

class ST7735:
    def __init__(self, spi, dc, cs, rst, width=128, height=128):
        self.spi = spi
        self.dc = Pin(dc, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.width = width
        self.height = height
        self.buffer = bytearray(self.height * self.width * 2)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)
        self._update_required = True
        self.init_display()

    def write_cmd(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytearray([data]) if isinstance(data, int) else data)
        self.cs.value(1)

    def init_display(self):
        self.rst.value(1)
        time.sleep(0.05)
        self.rst.value(0)
        time.sleep(0.05)
        self.rst.value(1)
        time.sleep(0.05)

        self.write_cmd(0x01)  # 软件复位
        time.sleep(0.15)

        self.write_cmd(0x11)  # 睡眠退出
        time.sleep(0.15)

        self.write_cmd(0x3A)  # 像素格式
        self.write_data(0x05)  # 16位

        self.write_cmd(0x36)  # 内存访问控制
        self.write_data(0xC8)

        self.write_cmd(0x29)  # 显示开启

    def show(self):
        x_offset = 2  # 微调左边白边
        y_offset = 3  # 微调下边白边

        x0 = x_offset
        y0 = y_offset
        x1 = x0 + self.width - 1
        y1 = y0 + self.height - 1

        self.write_cmd(0x2A)
        self.write_data(bytearray([0x00, x0, 0x00, x1]))
        self.write_cmd(0x2B)
        self.write_data(bytearray([0x00, y0, 0x00, y1]))
        self.write_cmd(0x2C)

        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(self.buffer)
        self.cs.value(1)
        self._update_required = False

    def fill(self, color):
        self.framebuf.fill(color)
        self._update_required = True

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)
        self._update_required = True

    def text(self, string, x, y, color):
        self.framebuf.text(string, x, y, color)
        self._update_required = True
        
    def circle(self, cx, cy, r, color):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    self.pixel(cx + x, cy + y, color)
        self._update_required = True

    async def auto_refresh(self, interval_ms=100):
        """异步自动刷新屏幕"""
        while True:
            if self._update_required:
                self.show()
            await asyncio.sleep_ms(interval_ms)


    

# 初始化硬件 SPI 和屏幕
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
tft = ST7735(spi, dc=13, cs=14, rst=12, width=128, height=128)

def draw_label_val(tft, label, value, x, y, color):
    tft.text(label, x, y, color)
    tft.text(str(value), x + len(label) * 8, y, color)  # 8 是字符宽度
        
async def draw_loop():
    count = 0
    current_freq = machine.freq()

    while True:
        tft.fill(0)
        tft.text("Async Count:", 10, 10, 0xFFFF)
        #tft.text(str(count), 10, 30, 0x07E0)
        draw_label_val(tft, "mem_free:", gc.mem_free(), 10, 50, 0x07E0)
        draw_label_val(tft, "mem_alloc:", gc.mem_alloc(), 10, 70, 0x07E0)            
        count += 1
        await asyncio.sleep(1)

async def main():
    # 启动自动刷新任务
    asyncio.create_task(tft.auto_refresh(100))
    # 启动绘图任务
    await draw_loop()

asyncio.run(main())
