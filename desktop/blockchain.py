import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce  # 用于挖矿的随机数
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty  # 挖矿难度（前缀0的数量）
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          timestamp=time.time(),
                          data=data,
                          previous_hash=last_block.hash)
        mined_block = self.proof_of_work(new_block)
        self.chain.append(mined_block)

    def proof_of_work(self, block):
        print(f"⛏️  Mining block #{block.index}...")
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        print(f"✅ Block #{block.index} mined: {block.hash}")
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True


if __name__ == "__main__":

    # 创建一个区块链
    my_chain = Blockchain(difficulty=3)

# 添加一些区块
    my_chain.add_block("First block data")
    my_chain.add_block("Second block data")

# 验证区块链是否有效
    print("Blockchain valid:", my_chain.is_chain_valid())

# 查看区块链内容
    for block in my_chain.chain:
      print(f"Index: {block.index}, Hash: {block.hash}, Data: {block.data}")
