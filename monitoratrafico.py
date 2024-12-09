from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para realizar o ping para o endereço 8.8.8.8
def check_trafic():
  
    try:
        # Executa o comando ping corretamente
        trafic_result = connection(cmd='/interface/monitor-traffic', interface='ether1',  duration=4)
        print("Monitoramento de trafico ether1 iniciado. Resultados:")

        # Processa os resultados do comando
        for response in trafic_result:
            # Obtém o tempo de resposta para cada pacote de ping
          #  trafic_bps = response.get('rx-bits-per-second', 'N/A')
          #  print(f"Tempo de monitor-traffic: {trafic_bps} bps")

            
                    rx_bps = response.get('rx-bits-per-second', 'N/A')  # Tráfego de download
                    tx_bps = response.get('tx-bits-per-second', 'N/A')  # Tráfego de upload
                    print(f"Interface: ether1, RX: {rx_bps} bps, TX: {tx_bps} bps")

    except Exception as e:
        print(f"Erro ao realizar monitor-traffic: {e}")

# Executando a função
check_trafic()
