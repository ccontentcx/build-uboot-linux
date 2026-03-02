import struct

# 定义我们最简单的格式的常量
PREAMBLE = b'\xde\xad\xbe\xef'  # 4个字节的固定包头
MAX_PAYLOAD_SIZE = 255          # 最大数据负载长度，因为我们用1个字节来存储长度

def calculate_checksum(data):
    """
    计算一个简单的校验和（所有字节的和对256取模）。
    """
    return sum(data) % 256

def encode_message(message_str):
    """
    将一个字符串消息按照我们的格式进行编码。
    """
    payload = message_str.encode('utf-8')
    payload_len = len(payload)

    if payload_len > MAX_PAYLOAD_SIZE:
        print(f"错误: 消息太长了，最大长度为 {MAX_PAYLOAD_SIZE} 字节。")
        return None

    # 计算校验和
    checksum = calculate_checksum(payload)

    # 将所有部分组合成最终的字节序列
    # '>' 表示大端字节序，'B' 表示一个无符号字符（1字节）
    length_byte = struct.pack('>B', payload_len)
    checksum_byte = struct.pack('>B', checksum)

    # 完整的数据包 = 包头 + 长度 + 负载 + 校验和
    encoded_packet = PREAMBLE + length_byte + payload + checksum_byte
    print("编码成功，生成的字节序列:", encoded_packet)
    return encoded_packet

def decode_message(encoded_packet):
    """
    将一个字节序列按照我们的格式进行解码。
    """
    # 检查包头是否正确
    if not encoded_packet.startswith(PREAMBLE):
        print("错误: 无效的包头。")
        return None

    # 提取长度和数据负载
    preamble_len = len(PREAMBLE)
    length_byte = encoded_packet[preamble_len:preamble_len + 1]
    payload_len = struct.unpack('>B', length_byte)[0]

    payload_start_index = preamble_len + 1
    payload_end_index = payload_start_index + payload_len
    payload = encoded_packet[payload_start_index:payload_end_index]

    # 提取并验证校验和
    received_checksum = struct.unpack('>B', encoded_packet[payload_end_index:payload_end_index + 1])[0]
    calculated_checksum = calculate_checksum(payload)

    if received_checksum != calculated_checksum:
        print("错误: 校验和不匹配，数据可能已损坏。")
        return None

    # 成功解码，返回消息字符串
    decoded_message = payload.decode('utf-8')
    return decoded_message

# --- 运行示例 ---
# 1. 编码一个消息
original_message = "你好，这是我设计的无线电格式！"
encoded_packet = encode_message(original_message)

if encoded_packet:
    print("原始消息:", original_message)
    print("编码后的字节串:", encoded_packet)

    # 2. 模拟传输后，进行解码
    # 假设这个字节串通过无线电波发送了出去...
    decoded_message = decode_message(encoded_packet)

    if decoded_message:
        print("解码后的消息:", decoded_message)