from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para adicionar a VLAN
def add_vlan():
    try:
        # Tentando adicionar a VLAN
        response = connection(cmd='/interface/vlan/add', name='vlan1000', interface='ether1', vlan_id=1000)

        # Verificando a resposta após o comando
        print("Comando enviado com sucesso!")

        # Exibindo a resposta completa
        print("Resposta do comando:")
        print(response)

        # Obtendo as VLANs configuradas após a tentativa de adicionar
        vlan_info = connection(cmd='/interface/vlan/print')
        if not vlan_info:
            print("Nenhuma VLAN configurada no momento.")
        else:
            print("Interfaces VLAN configuradas:")
            for vlan in vlan_info:
                print(f"VLAN: {vlan.get('name')}, Interface: {vlan.get('interface')}, VLAN ID: {vlan.get('vlan-id')}")
        
    except Exception as e:
        print(f"Erro ao adicionar VLAN: {e}")

# Executando a função para adicionar a VLAN
add_vlan()
