import socket
import threading

HOST = "localhost"  
PORT = 1100

clientes_conectados = []

clientes_info = {}

def transmitir_mensagem(mensagem, remetente_conexao, nome_do_remetente):

    mensagem_formatada = f"{nome_do_remetente}: {mensagem}"
    
    for cliente_socket in list(clientes_conectados):
        if cliente_socket != remetente_conexao:
            try:
                cliente_socket.sendall(mensagem_formatada.encode())
            except Exception as e:
                print(f"Erro ao enviar mensagem para {clientes_info.get(cliente_socket, 'Cliente Desconhecido')}: {e}")
                # Remover cliente se houver erro ao enviar
                if cliente_socket in clientes_conectados:
                    clientes_conectados.remove(cliente_socket)
                if cliente_socket in clientes_info:
                    del clientes_info[cliente_socket]
                try:
                    cliente_socket.close()
                except:
                    pass 

def lidar_com_cliente(conexao, endereco):
    nome_usuario_atual = ""
    try:
        # A primeira mensagem do cliente DEVE ser o nome de usuário
        dados_nome = conexao.recv(1024)
        if not dados_nome:
            print(f"Cliente {endereco} desconectou antes de enviar o nome.")
            return # Fecha a thread se o nome não for enviado

        nome_usuario_atual = dados_nome.decode()
        
        clientes_conectados.append(conexao)
        clientes_info[conexao] = nome_usuario_atual
        
        print(f'{endereco} identificado como: {nome_usuario_atual}')
        
        transmitir_mensagem(f"entrou no chat!", conexao, nome_usuario_atual) # Ou use "Sistema" como nome_do_remetente

        while True:
            dados = conexao.recv(1024)
            if not dados: # Cliente desconectou
                break 
            mensagem_recebida = dados.decode()
            print(f'Recebido de {nome_usuario_atual} ({endereco}): {mensagem_recebida}')
            
            # Transmite a mensagem para os outros usando o nome do usuário atual
            transmitir_mensagem(mensagem_recebida, conexao, nome_usuario_atual)
            
    except ConnectionResetError:
        print(f"Conexão resetada por {nome_usuario_atual} ({endereco}).")
    except Exception as e:
        print(f"Erro com o cliente {nome_usuario_atual} ({endereco}): {e}")
    finally:
        if conexao in clientes_conectados:
            clientes_conectados.remove(conexao)
        # Pega o nome do usuário que está saindo do dicionário
        nome_que_saiu = clientes_info.pop(conexao, None) # Remove do dicionário e retorna o nome
        
        if nome_que_saiu: # Se o nome foi encontrado
            print(f"Conexão com {nome_que_saiu} ({endereco}) fechada.")
            transmitir_mensagem(f"saiu do chat.", None, nome_que_saiu) # Envia para todos os restantes
        else:
            print(f"Conexão com {endereco} (sem nome identificado) fechada.")
        
        conexao.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print("Servidor aguardando conexões...")
    while True:
        conexao, endereco = servidor.accept()
        thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
        thread_cliente.start()