from db import executar_query
from utils import Obrigar_input, verificar_senha, gerar_hash_senha

def menu_empregados():
    while True:
        print("\n=== Menu de Empregados ===")
        print("1. Logar")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            logar_empregado()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def logar_empregado():
    print("\n=== Login de Empregado ===")
    cpf = input("CPF: ")
    senha = input("Senha: ")

    query = "SELECT * FROM Empregados WHERE CPF = %s"
    empregado = executar_query(query, (cpf,))

    if empregado and len(empregado) > 0 and verificar_senha(senha, empregado[0]['senha']):
        print(f"Bem-vindo(a), {empregado[0]['nome']}!")
        if empregado[0]['cargo'].lower() == 'administrador':
            menu_admin()
        else:
            menu_empregado_comum()
    else:
        print("CPF ou senha inválidos. Tente novamente.")

def menu_admin():
    while True:
        print("\n=== Menu do Administrador ===")
        print("1. Cadastrar novo empregado")
        print("2. Consultar empregados")
        print("3. Deletar empregado por nome")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_empregado()
        elif opcao == "2":
            consultar_empregados()
        elif opcao == "3":
            deletar_empregado_por_nome()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastrar_empregado():
    print("\n=== Cadastro de Novo Empregado ===")
    nome = Obrigar_input("Nome: ")
    cpf = Obrigar_input("CPF: ")
    cargo = Obrigar_input("Cargo: ")
    salario = float(Obrigar_input("Salário: "))
    data_admissao = Obrigar_input("Data de Admissão (AAAA-MM-DD): ")
    senha = Obrigar_input("Senha: ")
    hash_senha = gerar_hash_senha(senha)

    query = """
        INSERT INTO Empregados (Nome, CPF, Cargo, Salario, DataAdmissao, Senha)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        executar_query(query, (nome, cpf, cargo, salario, data_admissao, hash_senha))
        print("Novo empregado cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar empregado: {e}")

def consultar_empregados():
    print("\n=== Lista de Empregados ===")
    query = "SELECT * FROM Empregados ORDER BY Nome"
    try:
        resultados = executar_query(query)
        for empregado in resultados:
            print(f"Nome: {empregado['nome']}, CPF: {empregado['cpf']}, Cargo: {empregado['cargo']}, "
                  f"Salário: {empregado['salario']}, Data de Admissão: {empregado['dataadmissao']}")
    except Exception as e:
        print(f"Erro ao consultar empregados: {e}")

def deletar_empregado_por_nome():
    print("\n=== Deletar Empregado ===")
    nome = input("Digite as primeiras letras do nome do empregado: ")
    query = "DELETE FROM Empregados WHERE Nome LIKE %s"
    try:
        executar_query(query, (f"{nome}%",))
        print("Empregado(s) removido(s) com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar empregado: {e}")

def menu_empregado_comum():
    while True:
        print("\n=== Menu do Empregado Comum ===")
        print("1. Consultar Clientes")
        print("2. Consultar Entregadores")
        print("3. Consultar Restaurantes Afiliados")
        print("4. Deletar Cliente por Nome")
        print("5. Deletar Entregador por Nome")
        print("6. Deletar Restaurante por Nome")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            consultar_clientes()
        elif opcao == "2":
            consultar_entregadores()
        elif opcao == "3":
            consultar_restaurantes()
        elif opcao == "4":
            deletar_cliente_por_nome()
        elif opcao == "5":
            deletar_entregador_por_nome()
        elif opcao == "6":
            deletar_restaurante_por_nome()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def consultar_clientes():
    query = "SELECT nome, CPF, Telefone FROM Clientes"
    try:
        resultados = executar_query(query, ())
        print("\n=== Lista de Clientes ===")
        for cliente in resultados:
            print(f"Nome: {cliente['nome']}, CPF: {cliente['CPF']}, Telefone: {cliente['Telefone']}")
    except Exception as e:
        print(f"Erro ao consultar clientes: {e}")

def consultar_entregadores():
    query = "SELECT Nome, CPF, Telefone FROM Entregadores"
    try:
        resultados = executar_query(query, ())
        print("\n=== Lista de Entregadores ===")
        for entregador in resultados:
            print(f"Nome: {entregador['Nome']}, CPF: {entregador['CPF']}, Telefone: {entregador['Telefone']}")
    except Exception as e:
        print(f"Erro ao consultar entregadores: {e}")

def consultar_restaurantes():
    query = "SELECT Nome, Categoria, Telefone FROM RestaurantesAfiliados"
    try:
        resultados = executar_query(query, ())
        print("\n=== Lista de Restaurantes Afiliados ===")
        for restaurante in resultados:
            print(f"Nome: {restaurante['Nome']}, Categoria: {restaurante['Categoria']}, Telefone: {restaurante['Telefone']}")
    except Exception as e:
        print(f"Erro ao consultar restaurantes: {e}")




def deletar_cliente_por_nome():
    nome = input("Digite as primeiras letras do nome do cliente: ")
    query = "DELETE FROM Clientes WHERE Nome LIKE %s"
    try:
        executar_query(query, (f"{nome}%",))
        print("Cliente(s) removido(s) com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar cliente: {e}")

def deletar_entregador_por_nome():
    nome = input("Digite as primeiras letras do nome do entregador: ")
    query = "DELETE FROM Entregadores WHERE Nome LIKE %s"
    try:
        executar_query(query, (f"{nome}%",))
        print("Entregador(es) removido(s) com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar entregador: {e}")

def deletar_restaurante_por_nome():
    nome = input("Digite as primeiras letras do nome do restaurante: ")
    query = "DELETE FROM RestaurantesAfiliados WHERE Nome LIKE %s"
    try:
        executar_query(query, (f"{nome}%",))
        print("Restaurante(s) removido(s) com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar restaurante: {e}")
