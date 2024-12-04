from db import executar_query
from utils import Obrigar_input, verificar_senha, gerar_hash_senha

def menu_entregadores():
    while True:
        print("\n=== Menu de Entregadores ===")
        print("1. Cadastrar")
        print("2. Logar")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_entregador()
        elif opcao == "2":
            logar_entregador()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastrar_entregador():
    print("\n=== Cadastro de Entregador ===")
    nome = Obrigar_input("Nome: ")
    cpf = Obrigar_input("CPF: ")
    telefone = Obrigar_input("Telefone: ")

    usa_veiculo = input("\nVocê utiliza veículos emplacados para entregas? (s/n): ").strip().lower()
    if usa_veiculo == "s":
        tipo_veiculo = Obrigar_input("Tipo do Veículo (Ex: Moto, Carro, etc.): ")
        cnh = Obrigar_input("CNH: ")
        placa_veiculo = Obrigar_input("Placa do Veículo: ")
    else:
        tipo_veiculo = None
        cnh = None
        placa_veiculo = None

    senha = Obrigar_input("Senha: ")
    hash_senha = gerar_hash_senha(senha)

    query = """
        INSERT INTO Entregadores (Nome, CPF, Telefone, TipoVeiculo, CNH, PlacaVeiculo, Senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        executar_query(query, (nome, cpf, telefone, tipo_veiculo, cnh, placa_veiculo, hash_senha))
        print("Entregador cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar entregador: {e}")

def logar_entregador():
    print("\n=== Login de Entregador ===")
    cpf = input("CPF: ")
    senha = input("Senha: ")

    query = "SELECT * FROM Entregadores WHERE CPF = %s"
    entregador = executar_query(query, (cpf,))

    if entregador and verificar_senha(senha, entregador[0]['senha']):
        print(f"Bem-vindo(a), {entregador[0]['nome']}!")
        menu_entregador_logado()
    else:
        print("CPF ou senha inválidos. Tente novamente.")

def menu_entregador_logado():
    while True:
        print("\n=== Menu do Entregador ===")
        print("1. Consultar todos os restaurantes e seus endereços")
        print("2. Pesquisar cliente por nome para ver o endereço completo")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            consultar_restaurantes_com_enderecos()
        elif opcao == "2":
            pesquisar_cliente_por_nome()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def consultar_restaurantes_com_enderecos():
    print("\n=== Lista de Restaurantes com Endereços ===")
    query = """
        SELECT r.Nome AS Restaurante, r.Telefone AS TelefoneRestaurante, 
        e.Estado, e.Cidade, e.Bairro, e.Rua, e.Numero, e.CEP
        FROM RestaurantesAfiliados r
        JOIN Enderecos e ON r.EnderecoID = e.ID;
    """
    try:
        resultados = executar_query(query)
        if resultados:
            for restaurante in resultados:
                print(f"Restaurante: {restaurante['restaurante']}")
                print(f"Endereço: {restaurante['rua']}, {restaurante['numero']}")
                print(f"Bairro: {restaurante['bairro']}, Cidade: {restaurante['cidade']}/{restaurante['estado']}, CEP: {restaurante['cep']}\n")
        else:
            print("Nenhum restaurante encontrado.")
    except Exception as e:
        print(f"Erro ao consultar restaurantes: {e}")
 
def pesquisar_cliente_por_nome():
    print("\n=== Pesquisar Cliente ===")
    nome = input("Digite o nome ou parte do nome do cliente: ").strip()
    query = """
        SELECT c.Nome AS cliente, e.Rua, e.Numero, e.Bairro, e.Cidade, e.Estado, e.CEP
        FROM Clientes c
        JOIN Enderecos e ON c.EnderecoID = e.ID
        WHERE c.Nome LIKE %s
        ORDER BY c.Nome
    """
    try:
        resultados = executar_query(query, (f"%{nome}%",))
        print("Resultados brutos:", resultados)

        if resultados:
            for cliente in resultados:
                print(f"Cliente: {cliente.get('cliente', 'Desconhecido')}")
                print(f"Endereço: {cliente.get('rua', 'Desconhecido')}, {cliente.get('numero', 'Desconhecido')}")
                print(f"Bairro: {cliente.get('bairro', 'Desconhecido')}, Cidade: {cliente.get('cidade', 'Desconhecido')}/{cliente.get('estado', 'Desconhecido')}, CEP: {cliente.get('cep', 'Desconhecido')}\n")
        else:
            print("Nenhum cliente encontrado com esse nome.")
    except Exception as e:
        print(f"Erro ao pesquisar cliente: {e}")

