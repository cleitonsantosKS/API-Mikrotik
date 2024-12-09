from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para monitorar o tráfego em todas as interfaces
def check_traffic():
    try:
        # Obtém a lista de interfaces disponíveis
        interfaces = connection(cmd='/interface/print')

        # Itera sobre as interfaces para monitorar o tráfego
        for interface in interfaces:
            interface_name = interface.get('name')  # Nome da interface
            if not interface_name:
                continue  # Pula interfaces sem nome

            print(f"Monitorando tráfego para a interface: {interface_name}")

            try:
                # Monitora o tráfego da interface
                traffic_result = connection(cmd='/interface/monitor-traffic', interface=interface_name, duration=2)

                # Processa os resultados do monitoramento
                for response in traffic_result:
                    rx_bps = response.get('rx-bits-per-second', 'N/A')  # Tráfego de download
                    tx_bps = response.get('tx-bits-per-second', 'N/A')  # Tráfego de upload
                    print(f"Interface: {interface_name}, RX: {rx_bps} bps, TX: {tx_bps} bps")

            except Exception as monitor_error:
                print(f"Erro ao monitorar tráfego para {interface_name}: {monitor_error}")

    except Exception as e:
        print(f"Erro ao obter lista de interfaces: {e}")

# Executando a função
check_traffic()
