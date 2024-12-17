from librouteros import connect
import time
import os

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
        # Substitua 'admin' e a senha conforme necessário para o seu dispositivo
        connection = connect(username='admin', password='', host=ip)
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao MikroTik {ip}: {e}")
        return None

# Função para realizar o backup do MikroTik
def backup_mikrotik(connection, nome_host):
    try:
        # Obter a data e hora atual no formato desejado
        data_atual = time.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Definir o nome do arquivo de backup com o nome do host e a data/hora
        nome_arquivo = f"{nome_host}_backup_{data_atual}.backup"
        
        # Caminho onde o backup será armazenado localmente
        caminho_backup = f"./backups/{nome_arquivo}"
        
        # Criar diretório de backups, caso não exista
        if not os.path.exists('./backups'):
            os.makedirs('./backups')
        
        # Executar o comando de backup no MikroTik
        print(f"Iniciando o backup para {nome_host}...")
        connection(cmd='/system/backup/save', name=nome_arquivo)
        
        # Aguardar um tempo para garantir que o backup tenha sido gerado no MikroTik
        time.sleep(5)  # Pode ser ajustado conforme necessário
        
        # Usar o comando '/tool/fetch' para copiar o arquivo de backup para o caminho local
        print(f"Transferindo o backup de {nome_host} para o caminho local...")
        connection(cmd='/tool/fetch', url=f'ftp://{nome_arquivo}', dst_path=caminho_backup)
        
        print(f"Backup de {nome_host} concluído com sucesso. Arquivo salvo em: {caminho_backup}")
    
    except Exception as e:
        print(f"Erro ao realizar o backup para {nome_host}: {e}")

# Função principal para rodar o backup em todos os dispositivos
def realizar_backup_em_todos_os_dispositivos():
    print("Iniciando o backup...\n")
    
    # Ler os hosts do arquivo
    hosts = ler_hosts()
    
    # Realizar o backup para cada host
    for host in hosts:
        ip = host['ip']
        nome_host = host['nome']
        print(f"\nIniciando o backup para {nome_host} ({ip})...")
        
        # Conectar ao MikroTik
        connection = conectar_ao_mikrotik(ip)
        
        if connection:
            # Realizar o backup
            backup_mikrotik(connection, nome_host)
            print("\nBackup completo.\n")
        else:
            print(f"Não foi possível conectar ao MikroTik {nome_host} ({ip}).\n")

# Executando o backup em todos os dispositivos
realizar_backup_em_todos_os_dispositivos()
