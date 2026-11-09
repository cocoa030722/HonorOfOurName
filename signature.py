import sys
import os

def read_file(path):
    """
    :param path: 파일 경로
    :return: 청크 단위의 파일 스트림
    """
    pass


def show_file_info(file_stream):
    """
    :param file_stream: 청크 단위의 파일 스트림
    :return: void

    파일 스트림의 정보(파일명, 크기, 해시값) 표시
    """
    pass
def make_personal_key():
    """

    :return: 개인키
    """
    pass

def sign(file_stream, personal_key):
    """

    :param file_stream: 원본 파일 스트림
    :param personal_key: 개인키
    :return: 사인된 파일 스트림
    """
    pass

def main():
    if len(sys.argv) < 2:
        print(f"사용법: python {sys.argv[0]} <파일경로> <개인키 경로(optional)>")
        sys.exit(1)

    path = sys.argv[1]
    file_stream = read_file(path) # 파일 스트림의 구현?(라이브러리도 무방)
    show_file_info(file_stream)

    personal_key = None

    if len(sys.argv) < 3: # 개인키의 경로를 입력받았는지 여부 판정
        personal_key_path = sys.argv[2] # 개인키는 파일이라고 가정
        with open(personal_key_path, "r", encoding="utf-8") as f:
            personal_key = f.read()
    else:
        personal_key = make_personal_key()
        with open(os.getcwd(), "w", encoding="utf-8") as f:
            # 일단 현재 작업 디렉토리에 개인키를 저장하는 것으로 구현
            personal_key = f.read()

    sign(file_stream, personal_key) # 파일에 서명
    with open(os.getcwd(), "w", encoding="utf-8") as f:

        f.write(file_stream)
    print("서명된 파일이 저장되었습니다.")

if __name__ == '__main__':
    main()