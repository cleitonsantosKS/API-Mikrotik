from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para realizar o ping para o endereço 8.8.8.8
def check_ping():
    try:
        # Executa o comandiretamente no dispositivo MikroTik
        ping_result = connection(cmd='/ping', address='8.8.8.8', count=4)  # Comando direto em formato string
        print("Ping para 8.8.8.8 iniciado. Resultados:")

        # Processa o resultado do comando, que provavelmente será um iterável
        for response in ping_result:
            # Obtém os resultados de cada tentativa de ping
            time_ms = response.get('time', 'N/A')  # Tempo de resposta (ms)
            print(f"Tempo: {time_ms} ms")

    except Exception as e:
        print(f"Erro ao realizar ping: {e}")

# Executando a função
check_ping()
