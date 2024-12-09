from librouteros import connect
import time

# Conectar ao dispositivo MikroTik
# connection = connect(username='admin', password='', host='10.0.0.154')
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para verificar todas as interfaces (Ethernet, Wireless, etc.)
def check_interfaces():
    interfaces = connection('/interface/print')  # Obtém todas as interfaces
    for interface in interfaces:
        name = interface.get('name')  # Nome da interface
        status = interface.get('status')  # Status da interface
        comment = interface.get('comment')  # Comentário da interface
        
        print(f"Interface: {name}")
        print(f"Status: {status}")
        if comment:
            print(f"Comentário: {comment}")
        else:
            print("Comentário: Não configurado.")
        
        # Verifica se a interface está ativa (online)
        if status == 'link-ok':
            print(f"A interface {name} está online e operando normalmente.")
        else:
            print(f"Alerta: A interface {name} não está online!")

      #  print("\n")

# Função para verificar as rotas
def check_routes():
    routes = connection('/ip/route/print')  # Obtém as rotas IP
    for route in routes:
        dst_address = route.get('dst-address')  # Endereço de destino
        gateway = route.get('gateway')  # Gateway da rota
        
        print(f"Rota: {dst_address}")
        if gateway:
            print(f"Gateway: {gateway}")
        else:
            print("Alerta: Rota sem gateway configurado!")
      #  print("\n")

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
     #   print("\n")



# Função para verificar o uso de CPU
def check_cpu_usage():
    cpu_info = connection('/system/resource/print')  # Obtém as informações do CPU
    for cpu in cpu_info:
        cpu_load = cpu.get('cpu-load')  # A carga de CPU
        print(f"Carga do CPU: {cpu_load}%")
        if float(cpu_load) > 80:  # Se a carga do CPU for maior que 80%
            print("Alerta: A carga do CPU está alta!")
      #  print("\n")

def check_memory_usage():
    try:
        # Obtém as informações de sistema usando o comando correto
        memory_info = connection(cmd='/system/resource/print')

        # Itera sobre os resultados da consulta
        for memory in memory_info:
            total_memory = memory.get('total-memory')  # Memória total
            free_memory = memory.get('free-memory')
            uptime = memory.get('uptime')  # Memória livre
            
            # Calcula a memória usada
            used_memory = int(total_memory) - int(free_memory)

            # Converte bytes para megabytes
            total_memory_mb = int(total_memory) / (1024 * 1024)
            free_memory_mb = int(free_memory) / (1024 * 1024)
            used_memory_mb = used_memory / (1024 * 1024)

            # Exibe as informações de memória em MB
            print(f"uptime: {uptime} ")
            print(f"Memória Total: {total_memory_mb:.2f} MB")
            print(f"Memória Usada: {used_memory_mb:.2f} MB")
            print(f"Memória Livre: {free_memory_mb:.2f} MB")
            

            # Alerta caso a memória livre seja inferior a 500 MB
            if free_memory_mb < 500:  # Comparação em megabytes
                print("Alerta: Memória disponível baixa!")
         #   print("\n")

    except Exception as e:
        print(f"Erro ao verificar uso de memória: {e}")

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

# Função principal para rodar as verificações
def monitor_device():
    print("Iniciando monitoramento...\n")
    
   # check_interfaces()  # Verificar todas as interfaces
    print("\n")
    
    check_routes()  # Verificar as rotas
    print("\n")
    
    check_ping()  # Verificar ping para testar a conectividade externa
    # print("\n")
    
    check_cpu_usage()  # Verificar a carga de CPU
    print("\n")
    
    check_memory_usage()  # Verificar o uso de memória
    print("\n")

    check_traffic()


    print("\nMonitoramento finalizado.")

# Executando o monitoramento
monitor_device()
