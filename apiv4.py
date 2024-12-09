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

        print("\n")

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
        print("\n")
"""
# Função para verificar a latência (ping) para um endereço específico
def check_ping():
    target_ip = '8.8.8.8'  # Endereço de destino (exemplo: Google DNS)
    
    # Envia um ping para o destino
    result = connection('/ping', {'address': target_ip, 'count': 4})  # Realiza 4 pings para o destino
    
    print(f"Resultado do ping para {target_ip}:")
    for reply in result:
        if reply.get('status') == 'timeout':
            print(f"Erro: Não foi possível atingir {target_ip}.")
        else:
            print(f"Resposta de {target_ip}: tempo={reply.get('time')}ms")
    print("\n")
"""


# Função para verificar o uso de CPU
def check_cpu_usage():
    cpu_info = connection('/system/resource/print')  # Obtém as informações do CPU
    for cpu in cpu_info:
        cpu_load = cpu.get('cpu-load')  # A carga de CPU
        print(f"Carga do CPU: {cpu_load}%")
        if float(cpu_load) > 80:  # Se a carga do CPU for maior que 80%
            print("Alerta: A carga do CPU está alta!")
        print("\n")
"""
# Função para verificar o uso de memória
def check_memory_usage():
    memory_info = connection('/system/resource/print')  # Obtém as informações de memória
    for memory in memory_info:
        total_memory = memory.get('total-memory')  # Memória total
        used_memory = memory.get('used-memory')  # Memória usada
        free_memory = float(total_memory) - float(used_memory)  # Memória livre
        print(f"Memória Total: {total_memory} bytes")
        print(f"Memória Usada: {used_memory} bytes")
        print(f"Memória Livre: {free_memory} bytes")
        if free_memory < 500000000:  # Se a memória livre for inferior a 500MB
            print("Alerta: Memória disponível baixa!")
        print("\n")
"""
# Função principal para rodar as verificações
def monitor_device():
    print("Iniciando monitoramento...\n")
    
    check_interfaces()  # Verificar todas as interfaces
    print("\n")
    
    check_routes()  # Verificar as rotas
    print("\n")
    
    # check_ping()  # Verificar ping para testar a conectividade externa
    # print("\n")
    
    check_cpu_usage()  # Verificar a carga de CPU
    print("\n")
    
   # check_memory_usage()  # Verificar o uso de memória
    print("\nMonitoramento finalizado.")

# Executando o monitoramento
monitor_device()
