import socket
import threading

HOST = "localhost"
PORT = 1100

# ...
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print("Você entrou no chat! (digite 'sair' para desconectar)")
    nome_usuario = input("Digite seu nome de usuário: ")
    cliente.sendall(nome_usuario.encode()) # Envia o nome primeiro

    # Criar uma thread para receber mensagens do servidor continuamente
    def receber_mensagens(sock):
        while True:
            try:
                resposta = sock.recv(1024)
                if not resposta:
                    print("Desconectado do servidor.")
                    break
                print(resposta.decode())
            except:
                print("Erro ao receber mensagem ou conexão perdida.")
                break

    thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_recebimento.daemon = True # Permite que o programa principal saia mesmo se a thread estiver rodando
    thread_recebimento.start()

    while True:
        mensagem = input() # Não precisa mais do f"eco do servidor: {resposta.decode()}" aqui
        if mensagem.lower() == "sair":
            break
        cliente.sendall(mensagem.encode())

        