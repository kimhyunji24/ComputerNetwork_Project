import socket
import json

def send_message(sock, message):
    json_message = json.dumps(message)
    sock.send(json_message.encode())
    print(f"Sent: {json_message}")

def receive_message(sock):
    data = sock.recv(1024).decode()
    print(f"Received: {data}")
    return json.loads(data)


def get_user_choice():
    while True:
        try:
            choice = input("게임을 선택하세요\n1. 숫자야구\n2. 업다운\n선택: ")
            if choice in {'1', '2'}:
                return choice
            else:
                print("올바른 선택이 아닙니다. 다시 시도하세요.")
        except ValueError:
            print("올바른 선택이 아닙니다. 다시 시도하세요.")

def number_baseball_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    print("게임에 연결되었습니다.")

    choice = get_user_choice()
    client_socket.sendall(choice.encode())

    data = client_socket.recv(1024).decode()
    print(data)

    while True:
        if "정답입니다!" in data:
            break

        guess = input("숫자 3개를 입력하세요 (쉼표로 구분): ")
        client_socket.sendall(guess.encode())

        data = client_socket.recv(1024).decode()
        print(data)

    client_socket.close()

def up_down_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    print("게임에 연결되었습니다.")

    choice = get_user_choice()
    client_socket.sendall(choice.encode())

    data = client_socket.recv(1024).decode()
    print(data)

    while True:
        if "정답입니다!" in data:
            break

        guess = int(input("숫자를 입력하세요: "))
        client_socket.sendall(str(guess).encode())

        data = client_socket.recv(1024).decode()
        print(data)

    client_socket.close()

if __name__ == "__main__":
    game_choice = get_user_choice()

    if game_choice == "1":
        number_baseball_client()
    elif game_choice == "2":
        up_down_client()