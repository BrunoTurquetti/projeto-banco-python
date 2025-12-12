from banco import (
    buscar_conta_por_numero,
    realizar_transacao,
    consultar_saldo_detalhes # IMPORTADO DIRETO DE banco.py
)


def sacar_corrente(numero_conta, valor):
    """Implementa o saque para Conta Corrente (com limite de crédito)."""
    if valor <= 0:
        return "Erro: O valor do saque deve ser positivo."

    conta = buscar_conta_por_numero(numero_conta)
    
    if not conta or conta["tipo"] != "Corrente":
        return f"Erro: Conta {numero_conta} não é uma Conta Corrente válida."

    saldo_atual = conta["saldo"]
    limite = conta.get("limite_credito", 0.0)
    saldo_disponivel = saldo_atual + limite

    if valor > saldo_disponivel:
        return f" Erro: Saldo insuficiente. Saldo disponível (Saldo + Limite): R$ {saldo_disponivel:.2f}"
    
    # Executa o saque (permite que o saldo fique negativo)
    conta["saldo"] -= valor
    realizar_transacao(numero_conta, valor, "SAQUE CC")
    
    return f" Saque de R$ {valor:.2f} realizado na Conta Corrente {numero_conta}.\nNovo Saldo: R$ {conta['saldo']:.2f}"


def proximo_pagamento(numero_conta):
    """
    Implementa o método +proximoPagamento().
    Verifica o uso do limite de crédito e indica o valor a ser coberto.
    """
    
    # Reutiliza a função base para buscar os dados de forma segura
    conta_ou_erro = consultar_saldo_detalhes(numero_conta)
    if isinstance(conta_ou_erro, str):
        return conta_ou_erro # Retorna a mensagem de erro da função base
        
    if conta_ou_erro["tipo"] != "Corrente":
        return "Erro: Esta operação é exclusiva de Contas Correntes."
        
    saldo = conta_ou_erro["saldo"]
    
    if saldo >= 0:
        return f"Conta Corrente {numero_conta}: Saldo positivo de R$ {saldo:.2f}. Não há uso do limite de crédito no momento."
    else:
        valor_a_cobrir = abs(saldo)
        
        return f"⚠️ Limite de Crédito em Uso na Conta {numero_conta}!\n" \
               f"Valor negativo (uso do limite): R$ {saldo:.2f}\n" \
               f"Próximo pagamento necessário: R$ {valor_a_cobrir:.2f} para cobrir o saldo devedor."


def consultar_saldo_corrente(numero_conta):
    """Formata a consulta de saldo, adicionando a informação de limite e saldo disponível."""
    
    conta_ou_erro = consultar_saldo_detalhes(numero_conta)
    if isinstance(conta_ou_erro, str):
        return conta_ou_erro
        
    if conta_ou_erro["tipo"] != "Corrente":
        return "Erro: Conta informada não é Conta Corrente."

    saldo = conta_ou_erro["saldo"]
    limite = conta_ou_erro.get("limite_credito", 0.0)

    mensagem = f"--- SALDO DA CONTA {numero_conta} (Corrente) ---\n"
    mensagem += f"Saldo Atual: R$ {saldo:.2f}"
    mensagem += f"\nLimite de Crédito: R$ {limite:.2f}"
    mensagem += f"\nSaldo Total Disponível: R$ {saldo + limite:.2f}"
        
    return mensagem