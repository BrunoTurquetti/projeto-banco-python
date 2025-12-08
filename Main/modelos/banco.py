import datetime

# 1. Variáveis Globais (Os Dados do Banco)

CLIENTES = []
CONTAS = []
EMPRESTIMOS = []
TRANSACOES = [] # Nova lista para registrar as transações

# Contadores Globais
PROXIMO_ID_CLIENTE = 1
PROXIMO_NUMERO_CONTA = 1001
PROXIMO_ID_TRANSACAO = 1 # Novo contador
PROXIMO_ID_EMPRESTIMO = 1


# 2. Funções Auxiliares (Busca e Registro)

# Função que auxilia na busca pelo cliente na lista
def buscar_cliente_por_id(id_cliente):
    for cliente in CLIENTES:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    return None 

# Função que auxilia na busca pela CONTA na lista
def buscar_conta_por_numero(numero_conta):
    for conta in CONTAS:
        if conta["numero"] == numero_conta:
            return conta
    return None

# Função auxiliar para registrar todas as transações
def realizar_transacao(numero_conta, valor, tipo):
    global PROXIMO_ID_TRANSACAO
    
    nova_transacao = {
        "id_transacao": PROXIMO_ID_TRANSACAO,
        "numero_conta": numero_conta,
        "valor": valor,
        "tipo": tipo,
        "data_transacao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    TRANSACOES.append(nova_transacao)
    PROXIMO_ID_TRANSACAO += 1


# 3. Funções de Cadastro e Abertura 

# Função de cadastro de cliente
def cadastrar_cliente(nome, cpf, telefone, endereco):
    global PROXIMO_ID_CLIENTE
    
    novo_cliente = {
        "id_cliente": PROXIMO_ID_CLIENTE,
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "endereco": endereco
    }
    CLIENTES.append(novo_cliente)
    PROXIMO_ID_CLIENTE += 1
    return novo_cliente
    
# Função para abrir uma nova conta
def abrir_conta(id_cliente, tipo_conta="Corrente", saldo_inicial=0.0):
    global PROXIMO_NUMERO_CONTA
    
    cliente_existe = buscar_cliente_por_id(id_cliente)
    if not cliente_existe:
        print("Erro: Cliente não encontrado.")
        return None
        
    nova_conta = {
        "numero": str(PROXIMO_NUMERO_CONTA).zfill(4) + "-5",
        "saldo": saldo_inicial,
        "data_abertura": datetime.date.today().strftime("%Y-%m-%d"),
        "id_cliente": id_cliente,
        "tipo": tipo_conta,
    }

    if tipo_conta == "Corrente":
        nova_conta["limite_credito"] = 500.00
    elif tipo_conta == "Poupanca":
        nova_conta["taxa_juros"] = 0.005 # CORRIGIDO o erro de digitação
        
    CONTAS.append(nova_conta)
    PROXIMO_NUMERO_CONTA += 1
    return nova_conta


# Função: +concederEmprestimo (cliente: Cliente, emprestimo: Emprestimo)
def conceder_emprestimo(id_cliente, valor_emprestimo, taxa_juros, prazo_meses):
    global PROXIMO_ID_EMPRESTIMO

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return "Erro: Cliente não encontrado para conceder empréstimo."

    # Regra simples de negócio: Clientes só podem ter um empréstimo por vez (simplificação)
    for emp in EMPRESTIMOS:
        if emp["id_cliente"] == id_cliente and emp["status"] == "ATIVO":
             return "Erro: Cliente já possui um empréstimo ativo."

    # Cria o dicionário Emprestimo (conforme o diagrama)
    novo_emprestimo = {
        "id_emprestimo": PROXIMO_ID_EMPRESTIMO,
        "id_cliente": id_cliente,
        "valor_emprestimo": valor_emprestimo,
        "taxa_juros": taxa_juros,
        "prazo": prazo_meses,
        "data_concessao": datetime.date.today().strftime("%Y-%m-%d"),
        "parcela_mensal": (valor_emprestimo * (1 + taxa_juros * prazo_meses)) / prazo_meses,
        "status": "ATIVO"
    }

    EMPRESTIMOS.append(novo_emprestimo)
    PROXIMO_ID_EMPRESTIMO += 1
    
    # Aumentar o saldo da conta com o valor do empréstimo (opcional, dependendo da regra)
    # Aqui, a lógica é que o valor é creditado na primeira conta do cliente (para simplificar)
    conta_cliente = [c for c in CONTAS if c["id_cliente"] == id_cliente]
    if conta_cliente:
        conta = conta_cliente[0]
        conta["saldo"] += valor_emprestimo
        realizar_transacao(conta["numero"], valor_emprestimo, "CRÉDITO EMPRÉSTIMO")
    
    return f"Empréstimo de R$ {valor_emprestimo:.2f} concedido ao cliente {cliente['nome']}."

