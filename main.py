from modules import empregados, clientes, restaurantes, entregadores

def main_menu():
    while True:
        print("\n==== Sistema Nice :) ====")
        print("1. Empregados")
        print("2. Clientes")
        print("3. Restaurantes Afiliados")
        print("4. Entregadores")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            empregados.menu_empregados()
        elif opcao == "2":
            clientes.menu_clientes()
        elif opcao == "3":
            restaurantes.menu_restaurantes()
        elif opcao == "4":
            entregadores.menu_entregadores()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()
