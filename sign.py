import hashlib
import sys
import os
import argparse
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class InvalidAlgoError(Exception):
    pass # 유효한 알고리즘이 아님

# region cryptography 개인키 코드
"""
주의!: 이 코드에서는 학습을 위해 개인키를 바이너리 평문으로 다룹니다.
이 코드는 실제 전자서명 용도로 사용되어서는 안 됩니다. 
"""
def save_private_key_der(private_key, path: str) -> None:
    der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    # 생성 시점부터 소유자 전용(600) 권한, 기존 파일은 덮어쓰지 않음
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(der)


def load_private_key_der(path: str):
    return serialization.load_der_private_key(
        Path(path).read_bytes(), password=None
    )

def load_public_key_der(path: str):
    return serialization.load_der_public_key(Path(path).read_bytes())

PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH,
)
# endregion

def read_file(path) -> bytes:
    """
    :param path: 파일 경로
    :return: 파일 객체
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {p}")
    return p.read_bytes()


def show_file_info(path, file):
    """
    :param path: 파일명
    :param file: 바이너리 모드의 파일 객체
    :return: void

    파일의 정보(파일명, 크기, 해시값) 표시
    """
    print(f"파일명: {Path(path).name}")
    print(f"크기: {len(file)} bytes")


def sign(file, personal_key, enc_algo, hash_algo):
    """
    :param file: 원본 파일
    :param personal_key: 개인키
    :param enc_algo: 서명에 사용하는 알고리즘
    :return: 사인된 파일
    """
    if enc_algo not in ENC_CHOICES:
        raise InvalidAlgoError("유효하지 않은 암호 알고리즘")
    if hash_algo not in HASH_CHOICES:
        raise InvalidAlgoError("유효하지 않은 해시 알고리즘")

    hash_obj = None
    if hash_algo == "mock_hash":
        raise NotImplementedError("자체 제작 해시 알고리즘(구현되지 않음)")
    elif hash_algo == "sha256":
        hash_obj = hashes.SHA256()
    elif hash_algo == "sha384":
        hash_obj = hashes.SHA384()
    elif hash_algo == "sha512":
        hash_obj = hashes.SHA512()

    signature = None
    if enc_algo == "mock_enc":
        raise NotImplementedError("자체 제작 암호화 알고리즘(구현되지 않음)")
    elif enc_algo == "ecdsa":
        pass
    elif enc_algo == "rsa":
        signature = personal_key.sign(file, PSS, hash_obj)

    return signature


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

    file_path = args.file
    raw_file = read_file(file_path) # 파일 스트림은 일단 구현 안함
    show_file_info(file_path, raw_file)

    # 개인키의 경로는 항상 존재한다고 가정(없으면 오류)
    personal_key_path = args.key
    # 개인키를 알 수 없는 컨테이너 내의 객체로 다룸
    personal_key = load_private_key_der(personal_key_path)

    enc_algo = args.enc_algo
    signed_file = sign(raw_file, personal_key, enc_algo) # 파일에 서명
    with open(os.getcwd(), "w", encoding="utf-8") as f:
        f.write(signed_file)
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
        dest="hash_algo",
        choices=HASH_CHOICES,
        default=DEFAULT_HASH,
        help=f"해시 알고리즘 (기본값: {DEFAULT_HASH})",
    )
    parser.add_argument(
        "-e", "--encryption",
        dest="enc_algo",
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