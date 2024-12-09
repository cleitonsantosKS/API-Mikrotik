from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')

# Função para adicionar a VLAN
def add_vlan():
    try:
        # Adicionando a VLAN na interface especificada
        connection(cmd='/interface/vlan/ add', name='vlan1888', interface='ether1', vlan_id=1888)
        print("VLAN 1888 adicionada com sucesso!")

    except Exception as e:
        print(f"Erro ao adicionar VLAN: {e}")

# Executando a função para adicionar a VLAN
add_vlan()
