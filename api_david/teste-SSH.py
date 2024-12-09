import paramiko

# Configurações do dispositivo
host = "10.100.1.2"
#host = "192.168.142.135"  # Substitua pelo IP da sua antena
username = "root"  # Substitua pelo nome de usuário correto
passwords = [
    "ubnt1",  # Substitua pelas senhas que você quer testar
    "admin",
    "eve",
]

# Função para tentar autenticação SSH
def test_passwords(host, username, passwords):
    for password in passwords:
        print(f"Tentando senha: {password}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Aceita chaves de host desconhecidas
        try:
            # Tenta conectar com a senha atual
            ssh.connect(hostname=host, username=username, password=password, timeout=5)
            print(f"Senha correta encontrada: {password}")
            ssh.close()
            return password  # Retorna a senha correta
        except paramiko.AuthenticationException:
            print(f"Senha incorreta: {password}")
        except Exception as e:
            print(f"Erro ao conectar: {e}")
        finally:
            ssh.close()
    print("Nenhuma senha correta encontrada.")
    return None

# Testa as senhas
senha_correta = test_passwords(host, username, passwords)

if senha_correta:
    print(f"A senha correta é: {senha_correta}")
else:
    print("Falha ao encontrar a senha correta.")
