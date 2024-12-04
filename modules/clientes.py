from db import executar_query
from utils import Obrigar_input, verificar_senha, gerar_hash_senha

def menu_clientes():
    while True:
        print("\n=== Menu de Clientes ===")
        print("1. Cadastrar")
        print("2. Logar")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            logar_cliente()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastrar_cliente():
    print("\n=== Cadastro de Cliente ===")
    nome = Obrigar_input("Nome: ")
    cpf = Obrigar_input("CPF: ")
    telefone = Obrigar_input("Telefone: ")

    print("\nInforme seu endereço:")
    cep = Obrigar_input("CEP: ")
    estado = Obrigar_input("Estado: ")
    cidade = Obrigar_input("Cidade: ")
    bairro = Obrigar_input("Bairro: ")
    rua = Obrigar_input("Nome da Rua: ")
    numero = Obrigar_input("Número: ")

    senha = Obrigar_input("Senha: ")

    hash_senha = gerar_hash_senha(senha)

    endereco_query = """
        INSERT INTO Enderecos (Estado, Cidade, Bairro, Rua, Numero, CEP)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING ID
    """
    endereco_id = None
    
    try:
        endereco_id_result = executar_query(endereco_query, (estado, cidade, bairro, rua, numero, cep))
        if endereco_id_result:
            endereco_id = endereco_id_result['id']
        else:
            print("Erro ao cadastrar endereço.")
            return
    except Exception as e:
        print(f"Erro ao cadastrar endereço: {e}")
        return

    cliente_query = """
        INSERT INTO Clientes (Nome, CPF, Telefone, EnderecoID, Senha)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        executar_query(cliente_query, (nome, cpf, telefone, endereco_id, hash_senha))
        print("Cliente cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")

def logar_cliente():
    print("\n=== Login de Cliente ===")
    nome = input("Nome: ")
    senha = input("Senha: ")

    query = """
        SELECT ID, Senha FROM Clientes WHERE Nome = %s
    """
    cliente = executar_query(query, (nome,))

    if cliente:
        if 'senha' in cliente[0]:
            hash_armazenado = cliente[0]['senha']
            if verificar_senha(senha, hash_armazenado):
                print(f"Bem-vindo(a), {nome}!")
                cliente_id = cliente[0]['id']
                menu_cliente_logado(cliente_id)
            else:
                print("Nome ou senha inválidos. Tente novamente.")
        else:
            print("Erro: O campo 'senha' não foi encontrado no banco de dados.")
    else:
        print("Nome ou senha inválidos. Tente novamente.")

def menu_cliente_logado(cliente_id):
    while True:
        print("\n=== Menu do Cliente ===")
        print("1. Listar Restaurantes")
        print("2. Restaurantes e Seus Produtos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_restaurantes()
        elif opcao == "2":
            listar_restaurantes_com_produtos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")










def listar_restaurantes():
    print("\n=== Lista de Restaurantes ===")
    try:
        query = """
            SELECT Nome, Telefone, Categoria, EnderecoID 
            FROM RestaurantesAfiliados
        """
        restaurantes = executar_query(query, ())
        if restaurantes:
            for restaurante in restaurantes:
                print(f"Nome: {restaurante['nome']} | Telefone: {restaurante['telefone']} | Categoria: {restaurante['categoria']}")
        else:
            print("Nenhum restaurante encontrado.")
    except Exception as e:
        print(f"Erro ao listar restaurantes: {e}")





def listar_restaurantes_com_produtos():
    print("\n=== Restaurantes e Seus Produtos ===")
    try:
        query = """
            SELECT r.Nome AS Restaurante, p.Nome AS Produto 
            FROM RestaurantesAfiliados r
            JOIN Produtos p ON r.ID = p.RestauranteID
        """
        resultado = executar_query(query, ())
        if resultado:
            for item in resultado:
                print(f"Restaurante: {item['restaurante']} | Produto: {item['produto']}")
        else:
            print("Nenhum restaurante com produtos encontrado.")
    except Exception as e:
        print(f"Erro ao consultar restaurantes e produtos: {e}")
