import bcrypt

def Obrigar_input(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if entrada:
            return entrada
        print("Este campo é obrigatório. Por favor, insira um valor válido.")

def gerar_hash_senha(senha):
    salt = bcrypt.gensalt()
    hash_gerado = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_gerado.decode('utf-8')


def verificar_senha(senha, hash_armazenado):
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))
