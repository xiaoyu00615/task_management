"""
加密解密类模块
支持：AES 加密和简单加密
使用方式：导入此类后，实例化并传入密钥即可加密/解密
"""

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

class SimpleCryptor:
    """加密解密类，支持 AES 加密和简单加密"""

    def __init__(self, key, custom_char_set=None):
        """
        初始化加密解密器
        :param key: 密钥（str）
        :param custom_char_set: 自定义字符集（可选，仅用于简单加密）
        """
        # 初始化字符集（默认包含数字、大小写字母、常用特殊符号）
        self.default_char_set = (
            "0123456789"  # 数字
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 大写字母
            "abcdefghijklmnopqrstuvwxyz"  # 小写字母
            "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"  # 常用特殊符号
        )
        self.char_set = custom_char_set if custom_char_set else self.default_char_set
        self.char_len = len(self.char_set)  # 字符集长度（用于模运算）

        # 处理密钥
        self.key = self._process_key(key)
        # 生成 AES 密钥（32字节，用于 AES-256）
        self.aes_key = self._generate_aes_key(key)

    def _process_key(self, key):
        """私有方法：处理密钥，转为数字列表"""
        # 过滤出密钥中的纯数字，转为列表
        key_digits = [int(d) for d in str(key) if d.isdigit()]
        # 密钥为空/非数字时，用默认密钥
        if not key_digits:
            key_digits = [6, 8, 9]
        return key_digits

    def _generate_aes_key(self, key):
        """生成 AES 密钥"""
        # 使用 SHA-256 生成 32 字节的密钥
        import hashlib
        # 确保 key 是字符串类型
        if not isinstance(key, str):
            key = str(key)
        return hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        """
        加密方法：明文 → 密文（使用 AES 加密）
        :param plaintext: 明文
        :return: str 加密后的密文（base64 编码）
        """
        if not plaintext:
            return ""

        try:
            # 生成随机 IV（初始化向量）
            iv = os.urandom(16)
            # 创建 AES 加密器
            cipher = Cipher(
                algorithms.AES(self.aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            # 对数据进行填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext.encode()) + padder.finalize()
            
            # 加密数据
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            # 将 IV 和密文组合并 base64 编码
            combined = iv + ciphertext
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            # 如果 AES 加密失败，回退到简单加密
            return self._simple_encrypt(plaintext)

    def decrypt(self, ciphertext):
        """
        解密方法：密文 → 明文（使用 AES 解密）
        :param ciphertext: 加密后的密文（base64 编码）
        :return: str 解密后的明文
        """
        if not ciphertext:
            return ""

        try:
            # 解码 base64
            combined = base64.b64decode(ciphertext.encode('utf-8'))
            # 提取 IV 和密文
            iv = combined[:16]
            encrypted_data = combined[16:]
            
            # 创建 AES 解密器
            cipher = Cipher(
                algorithms.AES(self.aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # 解密数据
            padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # 移除填充
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            return plaintext.decode('utf-8')
        except Exception as e:
            # 如果 AES 解密失败，回退到简单解密
            return self._simple_decrypt(ciphertext)

    def _simple_encrypt(self, plaintext):
        """
        简单加密方法（备用）
        :param plaintext: 明文
        :return: str 加密后的密文
        """
        # 1. 逐字符处理：映射索引 → 移位运算
        processed = []
        for idx, char in enumerate(plaintext):
            # 字符集外的字符（如空格、中文）直接保留
            if char not in self.char_set:
                processed.append(char)
                continue

            # 字符 → 索引
            char_idx = self.char_set.index(char)
            # 取当前密钥位（循环使用）
            key_digit = self.key[idx % len(self.key)]
            # 移位加密：索引 + 密钥位 → 模字符集长度（避免越界）
            new_idx = (char_idx + key_digit) % self.char_len
            # 新索引 → 字符
            processed.append(self.char_set[new_idx])

        # 2. 反转结果（增加一层简单混淆）
        ciphertext = ''.join(processed[::-1])
        return ciphertext

    def _simple_decrypt(self, ciphertext):
        """
        简单解密方法（备用）
        :param ciphertext: 加密后的密文
        :return: str 解密后的明文
        """
        # 1. 先反转密文（还原加密时的反转操作）
        reversed_cipher = ciphertext[::-1]

        # 2. 逐字符处理：映射索引 → 移位还原
        processed = []
        for idx, char in enumerate(reversed_cipher):
            # 字符集外的字符直接保留
            if char not in self.char_set:
                processed.append(char)
                continue

            # 字符 → 索引
            char_idx = self.char_set.index(char)
            # 取当前密钥位（循环使用）
            key_digit = self.key[idx % len(self.key)]
            # 移位解密：索引 - 密钥位 → 模字符集长度（处理负数）
            new_idx = (char_idx - key_digit) % self.char_len
            # 新索引 → 字符
            processed.append(self.char_set[new_idx])

        plaintext = ''.join(processed)
        return plaintext

    def update_key(self, new_key):
        """
        更新密钥
        :param new_key: 新的密钥
        """
        self.key = self._process_key(new_key)
        self.aes_key = self._generate_aes_key(new_key)

    def get_char_set(self):
        """获取当前使用的字符集"""
        return self.char_set


# 测试示例（直接运行此模块时执行）
if __name__ == "__main__":
    # 1. 实例化加密器（传入自定义密钥）
    cryptor = SimpleCryptor(key="my_secret_key_123")

    # 2. 待加密的内容
    my_plain = "Hello, World! This is a test."

    # 3. 加密
    my_cipher = cryptor.encrypt(my_plain)
    print(f"原始明文：{my_plain}")
    print(f"加密密文：{my_cipher}")

    # 4. 解密
    my_decrypt = cryptor.decrypt(my_cipher)
    print(f"解密明文：{my_decrypt}")

    # 5. 验证
    print("✅ 加密解密成功" if my_plain == my_decrypt else "❌ 出错了")

