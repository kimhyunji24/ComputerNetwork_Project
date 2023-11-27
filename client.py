import socket

def get_user_choice():
    while True:
        try:
            choice = input("게임을 선택하세요\n1. 숫자야구\n2. 업다운\n선택 (exit로 종료): ")
            if choice in {'1', '2', 'exit'}:
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

        guess = input("숫자 3개를 입력하세요 (숫자 사이에 공백 없이): ")
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

        guess = input("숫자를 입력하세요 (exit로 종료): ")
        if guess.lower() == 'exit':
            client_socket.sendall("-1".encode())
            break

        client_socket.sendall(guess.encode())

        data = client_socket.recv(1024).decode()
        print(data)

    client_socket.close()

if __name__ == "__main__":
    game_choice = get_user_choice()

    if game_choice == "1":
        number_baseball_client()
    elif game_choice == "2":
        up_down_client()
