import datetime

# 1. Variáveis Globais (Os Dados do Banco)

clientes = []
contas = []
emprestimos = []
transacoes = [] # Nova lista para registrar as transações

# Contadores Globais
proximo_id_cliente = 1
proximo_numero_conta = 1001
proximo_id_transacao = 1 # Novo contador
proximo_id_emprestimo = 1


# 2. Funções Auxiliares (Busca e Registro)

# Função que auxilia na busca pelo cliente na lista
def buscar_cliente_por_id(id_cliente):
    for cliente in clientes: 
         if cliente["id_cliente"] == id_cliente:
             return cliente
    return None

# Função que auxilia na busca pela CONTA na lista
def buscar_conta_por_numero(numero_conta):
    for conta in contas:
        if conta["numero"] == numero_conta:
            return conta
    return None

# Função auxiliar para registrar todas as transações
def realizar_transacao(numero_conta, valor, tipo):
    global proximo_id_transacao
    
    nova_transacao = {
        "id_transacao": proximo_id_transacao,
        "numero_conta": numero_conta,
        "valor": valor,
        "tipo": tipo,
        "data_transacao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transacoes.append(nova_transacao)
    proximo_id_transacao += 1


# 3. Funções de Cadastro e Abertura 

# Função de cadastro de cliente
def cadastrar_cliente(nome, cpf, telefone, endereco):
    global proximo_id_cliente
    
    novo_cliente = {
        "id_cliente": proximo_id_cliente,
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco
    }
    clientes.append(novo_cliente)
    proximo_id_cliente += 1
    return novo_cliente
    
# Função para abrir uma nova conta
def abrir_conta(id_cliente, tipo_conta="Corrente", saldo_inicial=0.0):
    global proximo_numero_conta
    
    cliente_existe = buscar_cliente_por_id(id_cliente)
    if not cliente_existe:
        print("Erro: Cliente não encontrado.")
        return None
        
    nova_conta = {
        "numero": str(proximo_numero_conta).zfill(4) + "-5",
        "saldo": saldo_inicial,
        "data_abertura": datetime.date.today().strftime("%Y-%m-%d"),
        "id_cliente": id_cliente,
        "tipo": tipo_conta,
    }

    if tipo_conta == "Corrente":
        nova_conta["limite_credito"] = 500.00
    elif tipo_conta == "Poupanca":
        nova_conta["taxa_juros"] = 0.005 # CORRIGIDO o erro de digitação
        
    contas.append(nova_conta)
    proximo_numero_conta += 1
    return nova_conta

def depositar(numero_conta, valor):
    """Implementa o método +depositar(valor: double)."""
    if valor <= 0:
        return "Erro: O valor do depósito deve ser positivo."

    conta = buscar_conta_por_numero(numero_conta)
    
    if not conta:
        return f"Erro: Conta número {numero_conta} não encontrada."
    
    # Executa o depósito
    conta["saldo"] += valor
    realizar_transacao(numero_conta, valor, "DEPÓSITO")
    
    return f"✅ Depósito de R$ {valor:.2f} realizado na conta {numero_conta}.\nNovo Saldo: R$ {conta['saldo']:.2f}"


def consultar_saldo_detalhes(numero_conta):
    """
    Função auxiliar que retorna o dicionário da conta.
    É usada por contaCorrente.py e poupanca_servicos.py.
    """
    conta = buscar_conta_por_numero(numero_conta)
    
    if not conta:
        # Retorna uma string de erro para que os módulos downstream possam tratar
        return f"Erro: Conta número {numero_conta} não encontrada."
        
    return conta