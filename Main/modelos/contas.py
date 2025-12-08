# Função: +depositar(valor: double)
def depositar(numero_conta, valor):
    conta = buscar_conta_por_numero(numero_conta)
    
    if conta is None:
        return "Erro: Conta não encontrada."
        
    if valor <= 0:
        return "Erro: O valor do depósito deve ser positivo."

    conta["saldo"] += valor
    realizar_transacao(numero_conta, valor, "DEPÓSITO")

    return f"Depósito de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}. Novo saldo: R$ {conta['saldo']:.2f}"

# Função: +sacar(valor: double)
def sacar(numero_conta, valor):
    conta = buscar_conta_por_numero(numero_conta)
    
    if conta is None:
        return "Erro: Conta não encontrada."
        
    if valor <= 0:
        return "Erro: O valor do saque deve ser positivo."

    saldo_disponivel = conta["saldo"]
    
    # Se for Conta Corrente, considera o limite de crédito
    if conta["tipo"] == "Corrente":
        saldo_disponivel += conta.get("limite_credito", 0.0)
    
    if valor > saldo_disponivel:
        return "Erro: Saldo insuficiente."
    
    conta["saldo"] -= valor
    realizar_transacao(numero_conta, valor, "SAQUE")

    return f"Saque de R$ {valor:.2f} realizado com sucesso na conta {numero_conta}. Novo saldo: R$ {conta['saldo']:.2f}"

# Função: +consultarSaldo()
def consultar_saldo(numero_conta):
    conta = buscar_conta_por_numero(numero_conta)
    
    if conta is None:
        return "Erro: Conta não encontrada."
        
    saldo = conta["saldo"]
    limite = conta.get("limite_credito", 0.0)
    
    mensagem = f"Conta {numero_conta} - Saldo Atual: R$ {saldo:.2f}"
    if conta["tipo"] == "Corrente":
        mensagem += f" (Limite de Crédito: R$ {limite:.2f})"
        
    return mensagem