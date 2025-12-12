import math
import datetime


# 1. IMPORTAÇÃO DOS DADOS E FUNÇÕES DO SEU ARQUIVO BANCO.PY

from banco import (
    clientes,               
    contas,                 
    emprestimos,            
    proximo_id_emprestimo,  
    buscar_cliente_por_id,  
    realizar_transacao      
)


# 2. FUNÇÃO DE CÁLCULO (A receita de juros)

def calcular_parcela_price(valor_emprestimo, taxa_juros, prazo_meses):
    """Calcula o valor fixo da parcela usando a Tabela Price (Juros Compostos)."""
    V = valor_emprestimo
    i = taxa_juros
    n = prazo_meses
    
    if i == 0:
        if n == 0: return 0.0
        return V / n
    
    try:
        denominador = 1 - math.pow((1 + i), -n)
        if denominador == 0:
            return 0.0
        numerador = V * i
        valor_parcela = numerador / denominador
        return valor_parcela
    except ValueError:
        return 0.0



# 3. FUNÇÃO DO BANCO (conceder_emprestimo)

def conceder_emprestimo(id_cliente, valor_emprestimo, taxa_juros, prazo_meses):
    # Apenas o contador que é modificado precisa do 'global'. 
    # As listas 'emprestimos' e 'contas' são acessadas via import.
    global proximo_id_emprestimo 

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return "Erro: Cliente não encontrado para conceder empréstimo."

    # Busca a conta do cliente
    conta_cliente_list = [c for c in contas if c.get("id_cliente") == id_cliente]
    if not conta_cliente_list:
        return "Erro: Cliente não possui conta aberta para receber o crédito."
    
    conta = conta_cliente_list[0]
        
    # Regras de Negócio / Validações
    for emp in emprestimos:
        if emp.get("id_cliente") == id_cliente and emp.get("status") == "ATIVO":
            return "Erro: Cliente já possui um empréstimo ativo."
    
    if valor_emprestimo <= 0 or prazo_meses <= 0 or taxa_juros < 0:
        return "Erro: Parâmetros do empréstimo inválidos."

    # Cálculo da Parcela
    parcela_mensal = calcular_parcela_price(valor_emprestimo, taxa_juros, prazo_meses)
    
    if parcela_mensal <= 0:
        return "Erro: O valor da parcela não pôde ser calculado."

    # Concessão e Registro
    novo_emprestimo = {
        "id_emprestimo": proximo_id_emprestimo,
        "id_cliente": id_cliente,
        "valor_emprestimo": valor_emprestimo,
        "taxa_juros": taxa_juros,
        "prazo": prazo_meses,
        "data_concessao": datetime.date.today().strftime("%Y-%m-%d"),
        "parcela_mensal": parcela_mensal, 
        "status": "ATIVO"
    }

    emprestimos.append(novo_emprestimo)
    proximo_id_emprestimo += 1
    
    # Crédito do valor na conta e registro da transação
    conta["saldo"] += valor_emprestimo
    realizar_transacao(conta["numero"], valor_emprestimo, "CRÉDITO EMPRÉSTIMO")
    
    return f" Empréstimo concedido ao cliente {cliente['nome']} (ID {id_cliente}).\n" \
           f"  Valor creditado: R$ {valor_emprestimo:.2f}.\n" \
           f"  Parcela Fixa (Price): R$ {parcela_mensal:.2f} por {prazo_meses} meses."



# 4. FUNÇÃO DO CLIENTE/INTERFACE (solicitar_emprestimo_menu)

def solicitar_emprestimo_menu():
    """Função de interface para o cliente inserir os dados de solicitação."""
    print("\n===== SOLICITAÇÃO DE EMPRÉSTIMO =====")
    
    try:
        id_cliente = int(input("Digite o ID do Cliente (para identificação): "))
    except ValueError:
        print(" Erro: ID de cliente inválido.")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print(f" Erro: Cliente com ID {id_cliente} não encontrado.")
        return

    try:
        valor = float(input("Valor do empréstimo desejado: R$ "))
        taxa = float(input("Taxa de Juros Mensal (Ex: 0.01 para 1%): "))
        prazo = int(input("Prazo em Meses: "))
    except ValueError:
        print(" Erro: Entradas inválidas. Digite valores numéricos corretos.")
        return

    # Chama a função principal de concessão do Banco
    resultado = conceder_emprestimo(id_cliente, valor, taxa, prazo)
    print(resultado)