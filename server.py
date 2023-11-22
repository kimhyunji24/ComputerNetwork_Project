from socket import *
import threading
import random

players = []

def number_baseball(player_socket):
    answer = str(random.randint(100, 999))
    attempts = 0

    player_socket.send("숫자야구 게임입니다. 세 자리 수를 맞춰보세요 (0~9 사이의 숫자 중복 없이): ".encode())

    while True:
        guess = player_socket.recv(1024).decode()
        attempts += 1

        if len(guess) != 3 or not guess.isdigit() or len(set(guess)) != 3:
            player_socket.send("세 자리 수를 정확히 입력하세요 (0~9 사이의 숫자 중복 없이).".encode())
            continue

        strikes = sum(a == b for a, b in zip(answer, guess))
        balls = sum(a in answer for a in guess) - strikes

        if strikes == 3:
            player_socket.send(f"축하합니다! {attempts}번만에 숫자를 맞추셨습니다.".encode())
            break
        else:
            player_socket.send(f"{strikes} 스트라이크, {balls} 볼입니다. 다시 시도하세요.".encode())
    player_socket.close()


def tic_tac_toe(player_socket):
    board = [" " for _ in range(9)]
    current_player = "X"

    def print_board():
        board_str = "\n---------\n".join([" | ".join(board[i:i + 3]) for i in range(0, 9, 3)])
        player_socket.send(board_str.encode())

    def check_winner():
        for row in range(0, 9, 3):
            if board[row] == board[row + 1] == board[row + 2] != " ":
                return True

        for col in range(3):
            if board[col] == board[col + 3] == board[col + 6] != " ":
                return True

        if board[0] == board[4] == board[8] != " " or board[2] == board[4] == board[6] != " ":
            return True

        return False

    def is_board_full():
        return " " not in board

    player_socket.send("틱택토 게임입니다. 준비중입니다.".encode())
    print_board()

    while True:
        move = int(player_socket.recv(1024).decode())

        if board[move] == " ":
            board[move] = current_player
            print_board()

            if check_winner():
                player_socket.send(f"{current_player} 플레이어가 이겼습니다!".encode())
                break
            elif is_board_full():
                player_socket.send("무승부입니다!".encode())
                break

            current_player = "O" if current_player == "X" else "X"
        else:
            player_socket.send("이미 선택된 위치입니다. 다시 선택하세요.".encode())
    player_socket.close()



def updown_game(player_socket):
    number_to_guess = random.randint(1, 100)
    attempts = 0

    player_socket.send("업다운 게임입니다. 1부터 100까지의 숫자 중 하나를 맞춰보세요.".encode())

    while True:
        guess = player_socket.recv(1024).decode()
        attempts += 1

        try:
            guess = int(guess)
        except ValueError:
            player_socket.send("숫자를 입력하세요.".encode())
            continue

        if guess < number_to_guess:
            player_socket.send("숫자가 너무 작습니다. 다시 시도하세요.".encode())
        elif guess > number_to_guess:
            player_socket.send("숫자가 너무 큽니다. 다시 시도하세요.".encode())
        else:
            player_socket.send(f"축하합니다! {attempts}번만에 숫자를 맞추셨습니다.".encode())
            break
    player_socket.close()





def handle_player(player_socket, player_number):
    # 게임 선택을 받아서 처리
    player_socket.send("게임을 선택하세요:\n1. 숫자야구\n2. 틱택토\n3. 업다운".encode())
    game_choice = player_socket.recv(1024).decode()

    if game_choice == '1':
        number_baseball(player_socket)
    elif game_choice == '2':
        tic_tac_toe(player_socket)
    elif game_choice == '3':
        updown_game(player_socket)
    else:
        player_socket.send("올바른 게임을 선택하세요.".encode())

    player_socket.send("종료".encode())
    player_socket.close()

# Server setup
serverSock = socket(AF_INET, SOCK_STREAM)
HOST = '127.0.0.1'
port = 43875
serverSock.bind((HOST, port))
serverSock.listen(2)

print('%d번 포트로 접속 대기중…' % port)

while True:
    connectionSock, addr = serverSock.accept()
    print(str(addr), '에서 접속되었습니다.')

    # 헤더 작성
    header = b'HEADER'
    headerSize = len(header).to_bytes(4, byteorder='big')
    connectionSock.sendall(headerSize + header)

    # 바디 작성
    body = b'BODY'
    bodySize = len(body).to_bytes(4, byteorder='big')
    connectionSock.sendall(bodySize + body)

    players.append(connectionSock)

    if len(players) == 2:
        break

for i, player_socket in enumerate(players):
    player_thread = threading.Thread(target=handle_player, args=(player_socket, i + 1))
    player_thread.start()