import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [1]Depositar
    [2]Sacar
    [3]Extrato
    [4]Nova conta
    [5]Novo usuário
    [6]Lista de contas
    [7]Sair
    => """
    return input(textwrap.dedent(menu_text))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n Operação falhou! O valor informado é inválido!!!")
    return saldo, extrato


def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("\ Operação falhou! Você não tem saldo suficiente!!!")
    elif valor > limite:
        print("\n Operação falhou! O valor do saque excede o limite!!!")
    elif numero_saques >= limite_saques:
        print("\n Operação falhou! Número máximo de saques excedido!!!")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n Operação falhou! O valor informado é inválido!!!")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\nEXTRATO".center(16, "="))
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print("\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=" *16)


def criar_usuario(usuarios, cpf, nome, data_nascimento, endereco):
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("\n Já existe usuário com esse CPF!!!")
        return usuarios
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")
    return usuarios


def criar_conta(agencia, numero_conta, cpf, usuarios, contas):
    usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
    if usuario:
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
        contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")
        return contas
    else:
        print("\n Usuário não encontrado, fluxo de criação de conta encerrado!!!")
    return contas


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES)

        elif opcao == "3":
            exibir_extrato(saldo, extrato)

        elif opcao == "4":
            cpf = input("Informe o CPF (somente número): ")
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            usuarios = criar_usuario(usuarios, cpf, nome, data_nascimento, endereco)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            cpf = input("Informe o CPF do usuário: ")
            contas = criar_conta(AGENCIA, numero_conta, cpf, usuarios, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
