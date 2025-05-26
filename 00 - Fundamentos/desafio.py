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
