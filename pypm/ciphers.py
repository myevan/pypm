from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, secret, block_size=32, padding='\0', encoding='base64'):
        self.cipher = AES.new(secret)
        self.block_size = block_size
        self.padding = padding
        self.encoding = encoding

    def encrypt(self, src_text):
        pad = src_text + (self.block_size - len(src_text) % self.block_size) * self.padding
        return self.cipher.encrypt(pad).encode(self.encoding)

    def decrypt(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.decode(self.encoding)).rstrip(self.padding)
