import sys
import os
import argparse

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

DEFAULT_KEY = "private_key.pem"
DEFAULT_HASH = "sha256"
DEFAULT_ENC = "rsa"

HASH_CHOICES = ["mock_hash", "sha256", "sha384", "sha512"]
ENC_CHOICES = ["mock_enc", "rsa", "ecdsa"]

def main():
    """
    CLI 도구의 사용법:
    python sign.py [서명할 파일 경로] [개인키 경로] -h(hash) [해시 알고리즘] -e(encryption) [암호화 알고리즘]
    개인키 경로, -h, -e는 선택사항(없으면 기본값을 사용)
    """
    args = parse_args()

    path = args.file
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

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="sign.py",
        description="파일에 전자서명을 생성합니다.",
        add_help=False,  # -h를 해시 옵션으로 쓰기 위해 기본 도움말 비활성화
    )
    parser.add_argument("file", help="서명할 파일 경로")
    parser.add_argument(
        "key",
        nargs="?",
        default=DEFAULT_KEY,
        help=f"개인키 경로 (기본값: {DEFAULT_KEY})",
    )
    parser.add_argument(
        "-h", "--hash",
        dest="hash_alg",
        choices=HASH_CHOICES,
        default=DEFAULT_HASH,
        help=f"해시 알고리즘 (기본값: {DEFAULT_HASH})",
    )
    parser.add_argument(
        "-e", "--encryption",
        dest="enc_alg",
        choices=ENC_CHOICES,
        default=DEFAULT_ENC,
        help=f"암호화 알고리즘 (기본값: {DEFAULT_ENC})",
    )
    parser.add_argument(
        "--help",
        action="help",
        help="도움말 출력",
    )

    # 옵션과 위치 인자가 섞여도 파싱되도록 intermixed 사용
    args = parser.parse_intermixed_args(argv)

    if not os.path.isfile(args.file):
        parser.error(f"서명할 파일을 찾을 수 없습니다: {args.file}")
    if not os.path.isfile(args.key):
        parser.error(f"개인키 파일을 찾을 수 없습니다: {args.key}")

    return args

if __name__ == '__main__':
    main()