
import sys
import os
import argparse

def make_key():
    pass

def main():
    """
    사용법:
    make_key.py [저장 경로] -e [사용 알고리즘]
    """
    args = parse_args()
    make_key()

DEFAULT_ENC = "rsa"

ENC_CHOICES = ["mock_enc", "rsa", "ecdsa"]

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="make_key.py",
        description="개인키 생성.",
        add_help=False,  # -h를 해시 옵션으로 쓰기 위해 기본 도움말 비활성화
    )
    parser.add_argument(
        "save_path",
        nargs="?",
        default=os.getcwd(),
        help=f"개인키 경로 (기본값(현 위치): {os.getcwd()})",
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

    if not os.path.isfile(args.save_path):
        parser.error(f"개인키를 저장할 위치를 찾을 수 없습니다: {args.file}")

    return args

if __name__ == '__main__':
    main()
