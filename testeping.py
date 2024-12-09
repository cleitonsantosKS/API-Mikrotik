from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.142.135')

# Função para realizar o ping para o endereço 8.8.8.8
def check_ping():
    try:
        # Executa o comando ping corretamente
        ping_result = connection(cmd='/ping', address='8.8.8.8', count=4)
        print("Ping para 8.8.8.8 iniciado. Resultados:")

        # Processa os resultados do comando
        for response in ping_result:
            # Obtém o tempo de resposta para cada pacote de ping
            time_ms = response.get('time', 'N/A')
            print(f"Tempo de resposta: {time_ms} ms")

    except Exception as e:
        print(f"Erro ao realizar ping: {e}")

# Executando a função
check_ping()
