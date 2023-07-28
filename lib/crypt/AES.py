import base64
from Crypto.Cipher import AES
 
#  bytes不是32的倍数那就补足为32的倍数
def add_to_32(value):
    while len(value) % 32 != 0:
            value += b'\x00'
    return value     # 返回bytes
 
 
# str转换为bytes超过32位时处理
def cut_value(org_str):
    org_bytes = str.encode(org_str)
    n = int(len(org_bytes) / 32)
    i = 0
    new_bytes = b''
    while n >= 1:
        i = i + 1
        new_byte = org_bytes[(i-1)*32:32*i-1]
        new_bytes += new_byte
        n = n - 1
    if len(org_bytes) % 32 == 0:                   # 如果是32的倍数，直接取值
        all_bytes = org_bytes
    elif len(org_bytes) % 32 != 0 and n>1:         # 如果不是32的倍数，每次截取32位相加，最后再加剩下的并补齐32位
        all_bytes = new_bytes + add_to_32 (org_bytes[i*32:])
    else:
        all_bytes = add_to_32 (org_bytes)          # 如果不是32的倍数，并且小于32位直接补齐
    return all_bytes
 
 
def AES_encrypt(org_str,key):
    # 初始化加密器
    aes = AES.new(cut_value(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(cut_value(org_str))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text
 
 
def AES_decrypt(secret_str,key):
    # 初始化加密器
    aes = AES.new(cut_value(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(secret_str.encode(encoding='utf-8'))
    # 执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypted_text
