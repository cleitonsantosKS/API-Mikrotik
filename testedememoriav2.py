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
            free_memory = memory.get('free-memory')  # Memória livre
            
            # Calcula a memória usada
            used_memory = int(total_memory) - int(free_memory)

            # Converte bytes para megabytes
            total_memory_mb = int(total_memory) / (1024 * 1024)
            free_memory_mb = int(free_memory) / (1024 * 1024)
            used_memory_mb = used_memory / (1024 * 1024)

            # Exibe as informações de memória em MB
            print(f"Memória Total: {total_memory_mb:.2f} MB")
            print(f"Memória Usada: {used_memory_mb:.2f} MB")
            print(f"Memória Livre: {free_memory_mb:.2f} MB")

            # Alerta caso a memória livre seja inferior a 500 MB
            if free_memory_mb < 500:  # Comparação em megabytes
                print("Alerta: Memória disponível baixa!")
            print("\n")

    except Exception as e:
        print(f"Erro ao verificar uso de memória: {e}")

# Executa a função
check_memory_usage()
