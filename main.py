#!/usr/bin/env python
from operacoes import inserir_nota

def opcoes():
    print('opcoes:')
    print('1 - adicionar nota')

def sair():
    print('Saindo ...')



def main():
    opcoes()  # Exibe as opções

    opcao_map = {
        1: inserir_nota,
        0: sair

    }

    try:
        opcao = int(input('opcao: '))
        # Obtém a função correspondente à opção escolhida ou opcao_invalida() se não encontrar
        acao = opcao_map.get(opcao, opcao_invalida)
        acao()  # Executa a função
        if opcao != 0:  # Se a opção não for sair, continua executando
            main()
    except ValueError:
        print('Opção inválida. Por favor, digite um número.')
        main()

def opcao_invalida():
    print('Opção inválida. Por favor, tente novamente.')


main()