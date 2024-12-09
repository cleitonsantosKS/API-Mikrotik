
from librouteros import connect
import time

# Função para ler o arquivo de hosts
def ler_hosts():
    hosts = []
    try:
        with open('hosts.txt', 'r') as file:
            for line in file:
                # Remove espaços e quebra de linha
                line = line.strip()
                if line:
                    # Divide o nome do host e o IP
                    nome, ip = line.split(',')
                    hosts.append({'nome': nome, 'ip': ip})
    except Exception as e:
        print(f"Erro ao ler arquivo de hosts: {e}")
    return hosts

# Conectar ao dispositivo MikroTik
def conectar_ao_mikrotik(ip):
    try:
        connection = connect(username='admin', password='', host=ip)
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao MikroTik {ip}: {e}")
        return None

# Função para realizar o ping
def check_ping(connection):
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

# Função para verificar todas as interfaces (Ethernet, Wireless, etc.)
def check_interfaces(connection):
    try:
        interfaces = connection(cmd='/interface/print')  # Obtém todas as interfaces
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

    except Exception as e:
        print(f"Erro ao verificar interfaces: {e}")

# Função para verificar o uso de memória
def check_memory_usage(connection):
    try:
        memory_info = connection(cmd='/system/resource/print')  # Obtém as informações de sistema
        for memory in memory_info:
            total_memory = memory.get('total-memory')
            free_memory = memory.get('free-memory')
            uptime = memory.get('uptime')
            
            used_memory = int(total_memory) - int(free_memory)

            # Converte bytes para megabytes
            total_memory_mb = int(total_memory) / (1024 * 1024)
            free_memory_mb = int(free_memory) / (1024 * 1024)
            used_memory_mb = used_memory / (1024 * 1024)

            print(f"\nUptime: {uptime}")
            print(f"Memória Total: {total_memory_mb:.2f} MB")
            print(f"Memória Usada: {used_memory_mb:.2f} MB")
            print(f"Memória Livre: {free_memory_mb:.2f} MB")

            if free_memory_mb < 500:
                print("Alerta: Memória disponível baixa!")
    except Exception as e:
        print(f"Erro ao verificar memória: {e}")

def check_cpu_usage(connection):
    cpu_info = connection('/system/resource/print')  # Obtém as informações do CPU
    for cpu in cpu_info:
        cpu_load = cpu.get('cpu-load')  # A carga de CPU
        print(f"Carga do CPU: {cpu_load}%")
        if float(cpu_load) > 80:  # Se a carga do CPU for maior que 80%
            print("Alerta: A carga do CPU está alta!")
      #  print("\n")

def check_traffic(connection):
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

def check_routes(connection):
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

# Função principal para rodar as verificações
def monitor_devices():
    print("Iniciando monitoramento...\n")
    
    # Ler os hosts do arquivo
    hosts = ler_hosts()
    
    # Realizar o ping para cada host
   
    
    # Verificar interfaces e recursos de cada dispositivo
    for host in hosts:
        ip = host['ip']
        print(f"\nVerificando {host['nome']} ({ip})...")
        
        # Conectar ao MikroTik
        connection = conectar_ao_mikrotik(ip)
        
        if connection:
          #  check_interfaces(connection)
            check_routes(connection)
            check_memory_usage(connection)
            print("\n")
            check_ping(connection)
            print("\n")
            check_cpu_usage(connection)
           # check_traffic(connection)



            print("\nMonitoramento completo.\n")

# Executando o monitoramento dos dispositivos
monitor_devices()
