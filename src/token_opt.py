import hmac
import time
import base64
import hashlib

class TokenOPT:
    @staticmethod
    # Função para gerar o código OTP usando HMAC-SHA1
    def generate_otp(secret_key, interval=30):
        message = int(time.time()) // interval  # Tempo dividido pelo intervalo
        message_bytes = message.to_bytes(8, byteorder="big")
        secret_bytes = base64.b32decode(secret_key, casefold=True)
        hmac_hash = hmac.new(secret_bytes, message_bytes, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0F
        truncated_hash = hmac_hash[offset: offset + 4]
        otp = int.from_bytes(truncated_hash, byteorder="big") & 0x7FFFFFFF
        otp = str(otp).zfill(6)[-6:]  # Preenchimento com zeros à esquerda e truncamento para 6 dígitos
        return otp

    @staticmethod
    # Função para calcular o tempo restante até a próxima atualização
    def calculate_remaining_time(interval=30):
        current_time = int(time.time())
        remaining_time = interval - (current_time % interval)
        return remaining_time