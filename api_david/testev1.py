from librouteros import connect, exceptions

# Lista de senhas para testar
passwords = [
    'senha1',
    'senha2',
    'senha3',
    # Adicione mais senhas aqui
]

# Função para testar as senhas
def test_passwords():
    for password in passwords:
        try:
            print(f"Tentando senha: {password}")
            # Tenta conectar ao dispositivo MikroTik
            connection = connect(username='admin', password=password, host='10.100.1.2')
            print(f"Senha correta encontrada: {password}")
            return connection  # Retorna a conexão se a senha for correta
        except exceptions.TrapError as e:
            # Captura erro quando a senha está incorreta
            print(f"Senha incorreta: {password}")
        except Exception as e:
            # Captura outros erros (como problemas de conexão)
            print(f"Erro ao conectar: {e}")
    print("Nenhuma senha correta encontrada.")
    return None

# Verifica a conexão e testa as senhas
connection = test_passwords()

if connection:
    # Continua com a lógica se a conexão foi estabelecida
    print("Conexão bem-sucedida.")
else:
    # Lógica caso não tenha conseguido se conectar
    print("Falha ao conectar ao dispositivo. Verifique as credenciais.")
