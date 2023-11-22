from socket import *

# play_game 함수 정의
def play_game():
    print("게임을 선택하세요:\n1. 숫자야구\n2. 틱택토\n3. 업다운")
    choice = input("게임 번호를 입력하세요: ") # 입력을 정수로 변환
    return choice
# Client setup
from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
port = 43875

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((HOST, port))

print('접속 완료')

# 헤더 읽기
headerSize = int.from_bytes(clientSock.recv(4), byteorder='big')
header = clientSock.recv(headerSize)
print('헤더:', headerSize)

# 바디 읽기
bodySize = int.from_bytes(clientSock.recv(4), byteorder='big')
body = clientSock.recv(bodySize)
print('바디:', bodySize)


# 게임 선택을 받아서 서버에 전송
game_choice = play_game()
clientSock.send(str(game_choice)).encode()


while True:
    message = clientSock.recv(1024).decode()
    print(message)

    if message == "종료":
        break

    if "축하합니다" in message or "이겼습니다" in message or "무승부" in message:
        break

    guess = None

    # 게임 선택에 따라 입력 방식을 조정하여 서버에 전송
    if game_choice == 1:
        guess = input("숫자야구 게임입니다. 세 자리 수를 맞춰보세요 (0~9 사이의 숫자 중복 없이)")
    elif game_choice == 2:
        guess = int(input("0~8 중 빈 곳에 숫자를 입력하세요: "))  # 1~9 대신 0~8로 수정
    elif game_choice == 3:
        guess = int(input("1부터 100까지의 숫자를 입력하세요: "))


    clientSock.send(str(guess).encode())

clientSock.close()
