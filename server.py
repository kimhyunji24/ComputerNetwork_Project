import socket
import random

def handle_number_baseball(client_socket):
    answer = [random.randint(0, 9) for _ in range(3)]
    print("숫자야구 게임을 시작합니다. 정답:", answer)

    client_socket.sendall("게임을 시작합니다. 정답을 맞춰보세요.".encode())

    while True:
        guess = client_socket.recv(1024).decode()
        print("클라이언트가 추측한 숫자:", guess)

        if guess == 'exit':
            client_socket.sendall("게임을 종료합니다.".encode())
            break

        guess = [int(x) for x in guess]
        result = compare_number_baseball(answer, guess)

        client_socket.sendall(result.encode())

        if "정답입니다!" in result:
            break

def compare_number_baseball(answer, guess):
    if answer == guess:
        return "정답입니다!"

    strike = sum(a == b for a, b in zip(answer, guess))
    ball = sum(a in guess for a in answer) - strike

    return f"스트라이크: {strike}, 볼: {ball}"

def handle_up_down(client_socket):
    answer = random.randint(1, 100)
    print("업다운 게임을 시작합니다. 정답:", answer)

    client_socket.sendall("게임을 시작합니다. 정답을 맞춰보세요.".encode())

    while True:
        guess = int(client_socket.recv(1024).decode())
        print("클라이언트가 추측한 숫자:", guess)

        if guess == -1:
            client_socket.sendall("게임을 종료합니다.".encode())
            break

        result = compare_up_down(answer, guess)

        client_socket.sendall(result.encode())

        if "정답입니다!" in result:
            break

def compare_up_down(answer, guess):
    if answer == guess:
        return "정답입니다!"
    elif answer < guess:
        return "Down"
    else:
        return "Up"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen()

    print("서버 대기 중...")

    while True:
        client_socket, addr = server_socket.accept()
        print("클라이언트와 연결됨:", addr)

        game_choice = client_socket.recv(1024).decode()
        print("클라이언트의 게임 선택:", game_choice)

        if game_choice == "1":
            handle_number_baseball(client_socket)
        elif game_choice == "2":
            handle_up_down(client_socket)

        print("클라이언트와의 연결을 종료합니다.")
        client_socket.close()

if __name__ == "__main__":
    main()
