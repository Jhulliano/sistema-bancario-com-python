menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

# Constates
LIMITE_SAQUE = 3
LIMITE_RETIRADA = 500

# Variáveis
saldo = 0
extrato = []
numero_saques = 0

def depositar(saldo, extrato):
    valor_deposito = float(input("Informe o valor do depósito: R$ "))
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato.append(f"Depósito: R${valor_deposito:.2f}")
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
    else:
        print("Valor de depósito inválido. Tente novamente.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques):
    valor_saque = float(input("Informe o valor do saque: R$ "))

    excedeu_saldo = valor_saque > saldo
    excedeu_limite = valor_saque > LIMITE_RETIRADA
    excedeu_saques = numero_saques > LIMITE_SAQUE

    if excedeu_saldo:
        print("Você não tem saldo suficiente para realizar essa operação.")
    elif excedeu_limite:
        print("Você excedeu o limite de retirada diária.")
    elif excedeu_saques:
        print("Você excedeu o número de saques diários.")
    elif valor_saque > 0:
        saldo -= valor_saque
        extrato.append(f"Saque: R${valor_saque:.2f}")
        numero_saques += 1
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
    else:
        print("Valor de saque inválido. Tente novamente.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("EXTRATO".center(16, "="))
    print("Não foram realizados movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=" *16)

while True:
    opcao = input(menu)

    if opcao == "1":
        saldo, extrato = depositar(saldo, extrato)
    elif opcao == "2":
        saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques)
    elif opcao == "3":
        exibir_extrato(saldo, extrato)
    elif opcao == "4":
        print("Obrigado por usar nosso sistema bancário. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")
