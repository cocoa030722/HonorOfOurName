import sys

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

def main():
    if len(sys.argv) < 2:
        print(f"사용법: python {sys.argv[0]} <파일경로>")
        sys.exit(1)

    path = sys.argv[1]
    file_stream = read_file(path)
    show_file_info(file_stream)

if __name__ == '__main__':
    main()