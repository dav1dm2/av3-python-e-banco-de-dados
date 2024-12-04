from utils import gerar_hash_senha


senha = "admin123"
hash_senha = gerar_hash_senha(senha).decode('utf-8')
print(f"Hash gerado: {hash_senha}")




