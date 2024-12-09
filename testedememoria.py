from librouteros import connect

# Conectar ao dispositivo MikroTik
connection = connect(username='admin', password='', host='192.168.1.55')


def check_memory_usage():
    try:
        # Obtém as informações de sistema usando o comando correto
        memory_info = connection(cmd='/system/resource/print')

        # Itera sobre os resultados da consulta
        for memory in memory_info:
            total_memory = memory.get('total-memory')  # Memória total
            free_memory = memory.get('free-memory')  # Memória usada
            
            # Calcula a memória livre
            used_memory = int(total_memory) - int(free_memory)

            # Exibe as informações de memória
            print(f"Memória Total: {total_memory} bytes")
            print(f"Memória Usada: {used_memory} bytes")
            print(f"Memória Livre: {free_memory} bytes")

            # Alerta caso a memória livre seja inferior a 500 MB
            if free_memory < 500 * 1024 * 1024:  # 500 MB em bytes
                print("Alerta: Memória disponível baixa!")
            print("\n")

    except Exception as e:
        print(f"Erro ao verificar uso de memória: {e}")

# Executa a função
check_memory_usage()
