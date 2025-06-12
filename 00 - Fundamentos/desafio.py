# Sistema Bancário com match-case

import os

# Função para limpar a tela no Windows
def limpar_tela():
    os.system('cls')

menu = """
================== MENU ==================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
==========================================
Escolha uma opção:
=> """

saldo = 0
limite = 1000
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 5

while True:
    limpar_tela()
    print(menu)
    opcao = input()

    match opcao:
        case "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")
            
            input("Pressione Enter para continuar...")
            limpar_tela()

        case "s":
            valor = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")
            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")
            
            input("Pressione Enter para continuar...")
            limpar_tela()

        case "e":
            limpar_tela()
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
            input("Pressione Enter para continuar...")
            limpar_tela()

        case "q":
            limpar_tela()
            print("Saindo do sistema. Até logo!")
            break

        case _:
            limpar_tela()
            print("Operação inválida, por favor selecione uma opção válida.")
            input("Pressione Enter para tentar novamente...")
            limpar_tela()


====================================================================================================================================
====================================================================================================================================
====================================================================================================================================

Sistema bancário com novas funções


import os
import json

ARQUIVO_DADOS = 'usuarios.json'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_dados(usuarios):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(usuarios, f, indent=4)

def aplicar_rendimento(saldo):
    rendimento = saldo * 0.10
    novo_saldo = saldo + rendimento
    print(f"\nRendimento aplicado: R$ {rendimento:.2f}")
    print(f"Novo saldo: R$ {novo_saldo:.2f}")
    return novo_saldo, rendimento

def historico_transacoes(transacoes, limite=5):
    print("\n======= HISTÓRICO DE TRANSAÇÕES =========")
    if not transacoes:
        print("Nenhuma transação registrada.")
    else:
        for t in transacoes[-limite:]:
            print(t)
    print("=========================================")

def alterar_senha(usuarios, username):
    atual = input("Digite a senha atual: ").strip()
    if atual == usuarios[username]["senha"]:
        nova = input("Nova senha: ").strip()
        usuarios[username]["senha"] = nova
        salvar_dados(usuarios)
        print("Senha alterada com sucesso.")
    else:
        print("Senha incorreta.")

def menu_principal():
    return """
====== MENU PRINCIPAL ======
[1] Login
[2] Cadastrar novo usuário
[3] Excluir usuário
[4] Alterar senha
[0] Sair
============================
Escolha uma opção:
=> """

def menu_usuario():
    return """
========= MENU DO USUÁRIO =========
[d] Depositar
[s] Sacar
[e] Extrato completo
[h] Histórico (últimas 5)
[c] Consultar saldo
[r] Aplicar rendimento (10%)
[q] Sair da conta
===================================
Escolha uma opção:
=> """

usuarios = carregar_dados()

while True:
    limpar_tela()
    print(menu_principal())
    opcao = input().strip()

    if opcao == "1":  # Login
        username = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        if username in usuarios and usuarios[username]["senha"] == senha:
            user = usuarios[username]
            print(f"Bem-vindo(a), {username}!")
            input("Pressione Enter para continuar...")

            while True:
                limpar_tela()
                print(menu_usuario())
                acao = input().lower()

                match acao:
                    case "d":
                        if user["num_transacoes"] >= 10:
                            print("Limite de transações atingido!")
                        else:
                            valor = float(input("Valor do depósito: "))
                            if valor > 0:
                                user["saldo"] += valor
                                user["transacoes"].append(f"Depósito: R$ {valor:.2f}")
                                user["num_transacoes"] += 1
                                salvar_dados(usuarios)
                                print("Depósito realizado com sucesso.")
                            else:
                                print("Valor inválido.")
                        input("Pressione Enter...")

                    case "s":
                        if user["num_transacoes"] >= 10:
                            print("Limite de transações atingido!")
                        else:
                            valor = float(input("Valor do saque: "))
                            if valor > user["saldo"]:
                                print("Saldo insuficiente.")
                            elif valor > 1000:
                                print("Limite de saque excedido.")
                            elif valor > 0:
                                user["saldo"] -= valor
                                user["transacoes"].append(f"Saque: R$ {valor:.2f}")
                                user["num_transacoes"] += 1
                                salvar_dados(usuarios)
                                print("Saque realizado com sucesso.")
                            else:
                                print("Valor inválido.")
                            input("Pressione Enter...")

                    case "e":
                        if user["num_transacoes"] >= 10:
                            print("Limite de transações atingido!")
                        else:
                            print("\n====== EXTRATO COMPLETO ======")
                            if not user["transacoes"]:
                                print("Nenhuma transação.")
                            else:
                                for t in user["transacoes"]:
                                    print(t)
                            print(f"\nSaldo: R$ {user['saldo']:.2f}")
                            user["num_transacoes"] += 1
                            salvar_dados(usuarios)
                            input("Pressione Enter...")

                    case "h":
                        historico_transacoes(user["transacoes"])
                        input("Pressione Enter...")

                    case "c":
                        print(f"\nSaldo atual: R$ {user['saldo']:.2f}")
                        input("Pressione Enter...")

                    case "r":
                        if user["num_transacoes"] >= 10:
                            print("Limite de transações atingido!")
                        else:
                            user["saldo"], rendimento = aplicar_rendimento(user["saldo"])
                            user["transacoes"].append(f"Rendimento (10%): +R$ {rendimento:.2f}")
                            user["num_transacoes"] += 1
                            salvar_dados(usuarios)
                        input("Pressione Enter...")

                    case "q":
                        print("Saindo da conta...")
                        break

                    case _:
                        print("Opção inválida.")
                        input("Pressione Enter...")

        else:
            print("Usuário ou senha incorretos.")
            input("Pressione Enter...")

    elif opcao == "2":  # Cadastrar
        username = input("Novo usuário: ").strip()
        if username in usuarios:
            print("Usuário já existe!")
        else:
            senha = input("Crie uma senha: ").strip()
            usuarios[username] = {
                "senha": senha,
                "saldo": 0,
                "transacoes": [],
                "num_transacoes": 0
            }
            salvar_dados(usuarios)
            print("Usuário cadastrado com sucesso.")
        input("Pressione Enter...")

    elif opcao == "3":  # Excluir
        username = input("Usuário a excluir: ").strip()
        if username in usuarios:
            senha = input("Digite a senha para confirmar: ").strip()
            if senha == usuarios[username]["senha"]:
                del usuarios[username]
                salvar_dados(usuarios)
                print("Usuário excluído com sucesso.")
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")
        input("Pressione Enter...")

    elif opcao == "4":  # Alterar senha
        username = input("Usuário: ").strip()
        if username in usuarios:
            alterar_senha(usuarios, username)
        else:
            print("Usuário não encontrado.")
        input("Pressione Enter...")

    elif opcao == "0":
        print("Encerrando o sistema.")
        break

    else:
        print("Opção inválida.")
        input("Pressione Enter...")


===================================================================================================================================
====================================================================================================================================
====================================================================================================================================

from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n Operacao falhou! Voce nao tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!")
            return True
        else:
            print("\n Operacao falhou! O valor informado e invalido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Deposito realizado com sucesso!")
            return True
        else:
            print("\n Operacao falhou! O valor informado e invalido.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operacao falhou! O valor de saque excede o limite.")
        elif excedeu_saques:
            print("\n Operacao falhou! Numero maximo de saques excedido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
Agencia:\t{self.agencia}
C/Corrente:\t{self.numero}
Titular:\t{self.cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

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
==================== MENU ====================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuario
[5] Nova Conta
[6] Listar Contas
[7] Sair
=> """
    return input(textwrap.dedent(menu))

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return None
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n Cliente nao encontrado!")
        return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n Cliente nao encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n Cliente nao encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================= EXTRATO =================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Nao foram realizadas movimentacoes.")
    else:
        for t in transacoes:
            print(f"{t['tipo']}:\n\tR$ {t['valor']:.2f}")
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=============================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente numero): ")
    if filtrar_cliente(cpf, clientes):
        print("\n Ja existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("\n Cliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n Cliente nao encontrado, fluxo de criacao de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))

def filtrar_cliente(cpf, clientes):
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            break
        else:
            print("\n Operacao invalida, selecione novamente.")

if __name__ == "__main__":
    main()
