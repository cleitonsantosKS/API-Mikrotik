#include <iostream>
#include <string>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

using namespace std;

// Função para inicializar o socket e conectar ao MikroTik
bool init_socket(SOCKET &sock, const string &ip, int port) {
    WSADATA wsaData;  // Estrutura de dados do Winsock
    sockaddr_in server;  // Estrutura de informações do servidor para conexão
    
    // Inicializa o Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "Falha ao inicializar Winsock\n";
        return false;
    }

    // Cria o socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        cerr << "Erro ao criar o socket\n";
        return false;
    }

    // Define os detalhes do servidor (IP e porta)
    server.sin_family = AF_INET;
    server.sin_port = htons(port);  // Porta da API (8728 por padrão)
    server.sin_addr.s_addr = inet_addr(ip.c_str());  // IP do MikroTik

    // Tenta conectar ao servidor
    if (connect(sock, (sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
        cerr << "Falha ao conectar ao servidor\n";
        return false;
    }

    return true;
}

// Função para enviar o comando de login (usuário e senha)
bool login(SOCKET sock, const string &username, const string &password) {
    string login_command = "/login";  // Comando de login da API do MikroTik
    string user_command = "=name=" + username;  // Parâmetro de nome de usuário
    string pass_command = "=password=" + password;  // Parâmetro de senha

    // Envia o comando de login e os parâmetros
    send(sock, login_command.c_str(), login_command.length(), 0);
    send(sock, user_command.c_str(), user_command.length(), 0);
    send(sock, pass_command.c_str(), pass_command.length(), 0);

    // Aqui, idealmente, você deveria processar a resposta do MikroTik para verificar se o login foi bem-sucedido
    // Para simplicidade, vamos apenas retornar verdadeiro assumindo que o login foi bem-sucedido.
    return true;  // Em um código real, você verificaria a resposta para confirmar se o login foi bem-sucedido
}

// Função para enviar um comando ao MikroTik
void send_command(SOCKET sock, const string &command) {
    send(sock, command.c_str(), command.length(), 0);
    cout << "Comando enviado: " << command << endl;
}

// Função principal
int main() {
    SOCKET sock;
    string ip = "10.0.0.154";  // IP do MikroTik (ajuste conforme necessário)
    int port = 8728;  // Porta padrão da API MikroTik
    string username = "admin";  // Nome de usuário para login
    string password = "";  // Senha para login

    // Inicializa o socket e tenta conectar ao MikroTik
    if (!init_socket(sock, ip, port)) {
        cerr << "Falha ao conectar ao MikroTik\n";
        return 1;
    }

    // Tenta fazer login com as credenciais fornecidas
    if (!login(sock, username, password)) {
        cerr << "Falha na autenticação\n";
        return 1;
    }

    // Envia um comando ao MikroTik (exemplo: listar interfaces)
    send_command(sock, "/interface/print");
    send_command(sock, "ip address/  print");

    // Fechar a conexão com o MikroTik
    closesocket(sock);
    WSACleanup();  // Limpa as configurações do Winsock

    return 0;
}
