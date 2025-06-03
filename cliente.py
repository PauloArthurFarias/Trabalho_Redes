import socket

HOST = "192.168.18.38"
PORT = 1100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    while True:
        mensagem = input()
        if mensagem.lower() == "sair":
            break
        cliente.sendall(mensagem.encode())
        resposta = cliente.recv(1024)
        print(f"eco do servidor: {resposta.decode()}")
        