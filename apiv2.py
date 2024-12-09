from librouteros import connect  

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='10.0.0.154')

# Função para verificar a velocidade das interfaces Ethernet
def check_ethernet_speed():
    interfaces = connection('/interface/ethernet/print')
    for interface in interfaces:
        if interface.get('status') == 'link-ok':  # Verificando se a interface está online
            speed = interface.get('speed')  # Pegando a velocidade da interface
            if speed == '10Mbps':
                print(f"Alerta: A interface {interface.get('name')} está operando a 10Mbps!")
            elif speed == '100Mbps':
                print(f"Alerta: A interface {interface.get('name')} está operando a 100Mbps!")
            elif speed == '1Gbps':
                print(f"A interface {interface.get('name')} está operando corretamente a 1Gbps.")

# Função para verificar o status das rotas
def check_routes():
    routes = connection('/ip/route/print')
    for route in routes:
        if route.get('dst-address') == '0.0.0.0/0':  # Verifica a rota padrão
            status = route.get('gateway')
            if not status:
                print("Alerta: Rota padrão está sem gateway!")
            else:
                print(f"Rota padrão está configurada corretamente com o gateway {status}.")

# Função para verificar o status do sinal wireless
def check_wireless_signal():
    wireless_interfaces = connection('/interface/wireless/print')
    for wifi in wireless_interfaces:
        if wifi.get('disabled') == 'false':  # Verifica se a interface wireless está habilitada
            signal_strength = wifi.get('signal-strength')
            if signal_strength:
                print(f"Sinal da interface {wifi.get('name')} é {signal_strength} dBm.")
                if int(signal_strength) < -75:
                    print(f"Alerta: A interface {wifi.get('name')} tem sinal fraco (abaixo de -75 dBm)!")

# Função principal para rodar as verificações
def monitor_device():
    print("Iniciando monitoramento...\n")
    
    check_ethernet_speed()  # Verificar a velocidade das interfaces Ethernet
    print("\n")
    
    check_routes()  # Verificar as rotas
    print("\n")
    
    check_wireless_signal()  # Verificar as interfaces wireless
    print("\nMonitoramento finalizado.")

# Executando o monitoramento
monitor_device()
