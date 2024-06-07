import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > self.saldo:
            print("\nOperação falhou!!! Não possui saldo para operação.")
            return False

        if valor <= 0:
            print("\nOperação falhou!!! Valor inválido.")
            return False

        self._saldo -= valor
        print("\n=== Saque bem sucedido!!! ===")
        return True
    
    def depositar(self, valor):
        if valor <= 0:
            print("\nOperação falhou!!! Valor inválido.")
            return False
        
        self._saldo += valor
        print("\n=== Depósito bem sucedido!!! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = sum(1 for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__)

        if valor > self.saldo:
            print("\nOperação falhou!!! Não possui saldo para operação.")
            return False

        if valor > self._limite:
            print("\nOperação falhou!!! Valor excede o limite.")
            return False
        
        if numero_saques >= self._limite_saques:
            print("\nOperação falhou!!! Limite de saques diários atingido.")
            return False

        return super().sacar(valor)
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ======== Menu ========
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tNovo Usuário
    [6]\tListar Contas
    [7]\tSair
    ===> """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!!!")
        return None
    
    return cliente.contas[0]


def realizar_operacao_cliente(clientes, operacao):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!!!")
        return None, None
    
    valor = float(input(f"Informe o valor da operação ({operacao}): "))
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return None, None
    
    transacao = Saque(valor) if operacao == "Saque" else Deposito(valor)
    return cliente, transacao


def depositar(clientes):
    cliente, transacao = realizar_operacao_cliente(clientes, "Depósito")
    if cliente and transacao:
        cliente.realizar_transacao(cliente.contas[0], transacao)


def sacar(clientes):
    cliente, transacao = realizar_operacao_cliente(clientes, "Saque")
    if cliente and transacao:
        cliente.realizar_transacao(cliente.contas[0], transacao)


def exibir_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!!!")
        return None
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\nCliente não possui conta!!!")
        return None
    
    print(" EXTRATO ".center(30, "="))

    transacoes = conta.historico.transacoes
    if not transacoes:
        print("\nNenhuma transação realizada!!!")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} em {transacao['data']}")

    print(f"\nSaldo:\n\rR$ {conta.saldo:.2f}")
    print("=" *30)


def criar_cliente(clientes):
    cpf = input("Informe o CPf (Somente Número): ")
    if filtrar_cliente(cpf, clientes):
        print("CPF já cadastrado!!!")
        return None
    
    nome = input("Informe o nome completo do cliente: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso!!! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!!!")
        return None
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com Sucesso!!! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    operacoes = {
        "1": depositar,
        "2": sacar,
        "3": exibir_extrato,
        "4": criar_cliente,
        "5": lambda clientes=clientes, contas=contas: criar_conta(len(contas) + 1, clientes, contas),
        "6": lambda clientes=clientes: listar_contas(contas)
    }

    while True:
        opcao = menu()

        if opcao in operacoes:
            operacoes[opcao](clientes)
        elif opcao == "7":
            break
        else:
            print("\nOpção inválida!!!")

main()
