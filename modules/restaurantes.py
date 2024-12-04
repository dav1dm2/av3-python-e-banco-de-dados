from db import executar_query
from utils import Obrigar_input, verificar_senha, gerar_hash_senha

def menu_restaurantes():
    while True:
        print("\n=== Menu de Restaurantes Afiliados ===")
        print("1. Cadastrar")
        print("2. Logar")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_restaurante()
        elif opcao == "2":
            logar_restaurante()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastrar_restaurante():
    print("\n=== Cadastro de Restaurante ===")
    nome = Obrigar_input("Nome do Restaurante: ")
    cnpj = Obrigar_input("CNPJ: ")
    telefone = Obrigar_input("Telefone: ")
    categoria = Obrigar_input("Categoria (ex: Pizzaria, Lanchonete, etc.): ")

    print("\nInforme o endereço do restaurante:")
    estado = Obrigar_input("Estado: ")
    cidade = Obrigar_input("Cidade: ")
    bairro = Obrigar_input("Bairro: ")
    rua = Obrigar_input("Nome da Rua: ")
    cep = Obrigar_input("CEP: ")
    numero = Obrigar_input("Número: ")

    senha = Obrigar_input("Senha: ")
    hash_senha = gerar_hash_senha(senha)

    try:
        query_endereco = """
            INSERT INTO Enderecos (Estado, Cidade, Bairro, Rua, Numero, CEP)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING ID
        """
        endereco_resultado = executar_query(query_endereco, (estado, cidade, bairro, rua, numero, cep))
        endereco_id = endereco_resultado['id']

        query_restaurante = """
            INSERT INTO RestaurantesAfiliados 
            (Nome, CNPJ, Telefone, Categoria, EnderecoID, Senha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        executar_query(query_restaurante, (nome, cnpj, telefone, categoria, endereco_id, hash_senha))
        
        print("Restaurante cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar restaurante: {e}")

def logar_restaurante():
    print("\n=== Login de Restaurante ===")
    nome = input("Nome do Restaurante: ")
    senha = input("Senha: ")

    query = "SELECT * FROM RestaurantesAfiliados WHERE Nome = %s"
    restaurante = executar_query(query, (nome,))

    if restaurante and 'nome' in restaurante[0]:
        if verificar_senha(senha, restaurante[0]['senha']):
            print(f"Bem-vindo(a), {restaurante[0]['nome']}!")
            menu_operacoes_restaurante(restaurante[0]['id'])
        else:
            print("Senha incorreta. Tente novamente.")
    else:
        print("Restaurante não encontrado. Verifique o nome.")

def menu_operacoes_restaurante(restaurante_id):
    while True:
        print("\n=== Menu de Operações do Restaurante ===")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Deletar Produto")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_produto(restaurante_id)
        elif opcao == "2":
            listar_produtos(restaurante_id)
        elif opcao == "3":
            deletar_produto(restaurante_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def adicionar_produto(restaurante_id):
    print("\n=== Adicionar Produto ===")
    nome = Obrigar_input("Nome do Produto: ")
    descricao = Obrigar_input("Descrição do Produto: ")
    preco = Obrigar_input("Preço do Produto (ex: 19.99): ")

    try:
        query = """
            INSERT INTO Produtos (Nome, Descricao, Preco, RestauranteID)
            VALUES (%s, %s, %s, %s)
        """
        executar_query(query, (nome, descricao, preco, restaurante_id))
        print("Produto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")

def listar_produtos(restaurante_id):
    print("\n=== Lista de Produtos ===")
    try:
        query = "SELECT * FROM Produtos WHERE RestauranteID = %s"
        produtos = executar_query(query, (restaurante_id,))
        if produtos:
            for produto in produtos:
                print(f"ID: {produto['id']} | Nome: {produto['nome']} | Preço: {produto['preco']:.2f}")
                print(f"Descrição: {produto['descricao']}\n")
        else:
            print("Nenhum produto encontrado.")
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")

def deletar_produto(restaurante_id):
    print("\n=== Deletar Produto ===")
    nome_produto = Obrigar_input("Nome do Produto a ser deletado: ")

    try:
        query = "DELETE FROM Produtos WHERE Nome = %s AND RestauranteID = %s"
        executar_query(query, (nome_produto, restaurante_id))
        print("Produto deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
