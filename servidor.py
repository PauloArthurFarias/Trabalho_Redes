import socket

HOST = "192.168.18.38"
PORT = 1100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print("Servidor aguardando conexão...")
    conexao, endereco = servidor.accept()
    with conexao:
        print(f'Conectado por {endereco}')
        while True:
            dados = conexao.recv(1024)
            if not dados:
                print("conexão encerrada.")
                break
            print(f'Recebido: {dados.decode()}')
            conexao.sendall(dados)

