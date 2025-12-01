# def login(user, senha):
#     pass

# def listaClientes(): Verificar se o cliente já tem cadastro
#     pass

def validador_cpf(cpf, cpf_valido):
    cpf_valido = False
    
    if len(cpf) == 11:
        contador_regressiva = 10
        contador_soma = 0
        
        for num in cpf[0:9]:
            contador_soma += contador_regressiva * int(num)
            contador_regressiva -= 1
        
        valor_primeiro_digito = contador_soma * 10 % 11
        resultado_valor_primeiro_digito = 0 if valor_primeiro_digito > 9 else valor_primeiro_digito
        
        if resultado_valor_primeiro_digito == int(cpf[-2]):
            contador_regressiva2 = 11
            contador_soma2 = 0
            
            for num in cpf[0:10]:
                contador_soma2 += contador_regressiva2 * int(num)
                contador_regressiva2 -= 1
            
            valor_segundo_digito = contador_soma2 * 10 % 11
            resultado_valor_segundo_digito = 0 if valor_segundo_digito > 9 else valor_segundo_digito
            
            if resultado_valor_segundo_digito == int(cpf[-1]):
                cpf_valido = True
            else:
                return cpf, cpf_valido
        
        else:
            return cpf, cpf_valido
    
    else:
        return cpf, cpf_valido
    
    return cpf, cpf_valido

def criarConta():
    cpf_valido = False
    cpf = ''
    tentar_novamente = True
    continuar_processo = True
    print("=====PROCESSO INICIAL DE CADASTRO DO CLIENTE=====\n")
    
    while not cpf_valido and tentar_novamente:
        cpf = input('Digite seu CPF: ') # tratamento de erro
        cpf, cpf_valido = validador_cpf(cpf, cpf_valido)
        
        if cpf_valido:
            print('CPF VALIDO!!\n')
            tentar_novamente = False
        else:
            print('CPF INVALIDO!!\n')
            continuar = input('Continuar [S] / Não Continuar [N]: ').upper()
            
            if continuar == 'S':
                continue
            else:
                continuar_processo = False
                break
    
    if continuar_processo:
        print('=====INSIRA SUA INFORMAÇÕES SOLICITADOS.=====\n')
        nome = input('Informe o seu nome: ')
        endereco = input('Informe o seu endereço: ')
        telefone = input('Informe o número de telefone: ') # tratamento de erro
        # tipo_conta = True if input('Conta Corrente [C] / Conta Salario [S]: ').upper() == 'C' else False
        print(nome, cpf, endereco, telefone)
        # list_clientes.append({"nome": nome, "cpf": cpf, "endereco": endereco, "telefone": telefone})
    else:
        print('VOU SAIR!!')

# def emprestimo():
#     pass

criarConta()
print('FINALIZADO')

