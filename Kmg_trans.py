import lzma
import os
import argparse
from typing import Optional
from pathlib import Path

MAGIC_HEADER = bytes([
    0x7c, 0xd5, 0x32, 0xeb, 0x86, 0x02, 0x7f, 0x4b, 0xa8, 0xaf, 0xa6, 0x8e, 0x0f, 0xff, 0x99,
    0x14, 0x00, 0x04, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00,
])
HEADER_LEN = 1024
PUB_KEY_LEN = 1170494464
PUB_KEY_LEN_MAGNIFICATION = 16
READ_BUFFER_SIZE = 16 * 1024

PUB_KEY_MEND = bytes([
    0xB8, 0xD5, 0x3D, 0xB2, 0xE9, 0xAF, 0x78, 0x8C, 0x83, 0x33, 0x71, 0x51, 0x76, 0xA0,
    0xCD, 0x37, 0x2F, 0x3E, 0x35, 0x8D, 0xA9, 0xBE, 0x98, 0xB7, 0xE7, 0x8C, 0x22, 0xCE,
    0x5A, 0x61, 0xDF, 0x68, 0x69, 0x89, 0xFE, 0xA5, 0xB6, 0xDE, 0xA9, 0x77, 0xFC, 0xC8,
    0xBD, 0xBD, 0xE5, 0x6D, 0x3E, 0x5A, 0x36, 0xEF, 0x69, 0x4E, 0xBE, 0xE1, 0xE9, 0x66,
    0x1C, 0xF3, 0xD9, 0x02, 0xB6, 0xF2, 0x12, 0x9B, 0x44, 0xD0, 0x6F, 0xB9, 0x35, 0x89,
    0xB6, 0x46, 0x6D, 0x73, 0x82, 0x06, 0x69, 0xC1, 0xED, 0xD7, 0x85, 0xC2, 0x30, 0xDF,
    0xA2, 0x62, 0xBE, 0x79, 0x2D, 0x62, 0x62, 0x3D, 0x0D, 0x7E, 0xBE, 0x48, 0x89, 0x23,
    0x02, 0xA0, 0xE4, 0xD5, 0x75, 0x51, 0x32, 0x02, 0x53, 0xFD, 0x16, 0x3A, 0x21, 0x3B,
    0x16, 0x0F, 0xC3, 0xB2, 0xBB, 0xB3, 0xE2, 0xBA, 0x3A, 0x3D, 0x13, 0xEC, 0xF6, 0x01,
    0x45, 0x84, 0xA5, 0x70, 0x0F, 0x93, 0x49, 0x0C, 0x64, 0xCD, 0x31, 0xD5, 0xCC, 0x4C,
    0x07, 0x01, 0x9E, 0x00, 0x1A, 0x23, 0x90, 0xBF, 0x88, 0x1E, 0x3B, 0xAB, 0xA6, 0x3E,
    0xC4, 0x73, 0x47, 0x10, 0x7E, 0x3B, 0x5E, 0xBC, 0xE3, 0x00, 0x84, 0xFF, 0x09, 0xD4,
    0xE0, 0x89, 0x0F, 0x5B, 0x58, 0x70, 0x4F, 0xFB, 0x65, 0xD8, 0x5C, 0x53, 0x1B, 0xD3,
    0xC8, 0xC6, 0xBF, 0xEF, 0x98, 0xB0, 0x50, 0x4F, 0x0F, 0xEA, 0xE5, 0x83, 0x58, 0x8C,
    0x28, 0x2C, 0x84, 0x67, 0xCD, 0xD0, 0x9E, 0x47, 0xDB, 0x27, 0x50, 0xCA, 0xF4, 0x63,
    0x63, 0xE8, 0x97, 0x7F, 0x1B, 0x4B, 0x0C, 0xC2, 0xC1, 0x21, 0x4C, 0xCC, 0x58, 0xF5,
    0x94, 0x52, 0xA3, 0xF3, 0xD3, 0xE0, 0x68, 0xF4, 0x00, 0x23, 0xF3, 0x5E, 0x0A, 0x7B,
    0x93, 0xDD, 0xAB, 0x12, 0xB2, 0x13, 0xE8, 0x84, 0xD7, 0xA7, 0x9F, 0x0F, 0x32, 0x4C,
    0x55, 0x1D, 0x04, 0x36, 0x52, 0xDC, 0x03, 0xF3, 0xF9, 0x4E, 0x42, 0xE9, 0x3D, 0x61,
    0xEF, 0x7C, 0xB6, 0xB3, 0x93, 0x50,
])

_pub_key = None


def load_public_key(xz_path: str = "kugou_key.xz") -> bytes:
    global _pub_key
    if _pub_key is not None:
        return _pub_key

    if not os.path.exists(xz_path):
        raise FileNotFoundError(f"找不到公钥文件 {xz_path}")

    with lzma.open(xz_path, "rb") as f:
        _pub_key = f.read()

    expected_len = PUB_KEY_LEN // PUB_KEY_LEN_MAGNIFICATION
    if len(_pub_key) != expected_len:
        raise ValueError(f"公钥长度不匹配，预期 {expected_len} 字节，实际 {len(_pub_key)} 字节")

    return _pub_key


class KuGouDecoder:
    def __init__(self, input_stream, key_xz_path: str = "kugou_key.xz"):
        self.pub_key = load_public_key(key_xz_path)
        self.pub_mend_len = len(PUB_KEY_MEND)
        self.origin = input_stream
        self.pos = 0

        header = self.origin.read(HEADER_LEN)
        if len(header) != HEADER_LEN or not header.startswith(MAGIC_HEADER):
            raise ValueError("无效的KGM加密文件")

        self.own_key = bytearray(header[0x1c:0x2c])
        self.own_key.append(0)
        self.own_key_len = len(self.own_key)

    @classmethod
    def try_new(cls, input_stream, key_xz_path: str = "kugou_key.xz") -> Optional["KuGouDecoder"]:
        try:
            return cls(input_stream, key_xz_path)
        except Exception:
            return None

    def read(self, size: int = -1) -> bytes:
        encrypted = self.origin.read(size)
        if not encrypted:
            return b""

        decrypted = bytearray(len(encrypted))
        for i in range(len(encrypted)):
            current_pos = self.pos + i
            b = encrypted[i]

            own = b ^ self.own_key[current_pos % self.own_key_len]
            own ^= (own & 0x0F) << 4

            pub_idx = current_pos // PUB_KEY_LEN_MAGNIFICATION
            pub_byte = self.pub_key[pub_idx] ^ PUB_KEY_MEND[current_pos % self.pub_mend_len]
            pub_byte ^= (pub_byte & 0x0F) << 4

            decrypted[i] = own ^ pub_byte

        self.pos += len(encrypted)
        return bytes(decrypted)


def detect_audio_format(header: bytes) -> str:
    if len(header) < 128:
        return "mp3"

    if header.startswith(b"fLaC"):
        return "flac"
    if header.startswith(b"RIFF") and header[8:12] == b"WAVE":
        return "wav"
    if header.startswith(b"OggS"):
        return "ogg"
    if header[:2] in (b"\xff\xf1", b"\xff\xf9"):
        return "aac"
    if header.startswith(b"ID3") or header[:2] == b"\xff\xfb":
        return "mp3"

    return "mp3"


def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("请输入 y 或 n")


def get_all_files(target: str, recursive: bool) -> list[str]:
    files = []
    path = Path(target)

    if not path.exists():
        print(f'Invalid: "{target}", 路径不存在')
        return files

    if path.is_file():
        files.append(str(path))
        return files

    if path.is_dir():
        if recursive:
            for root, _, filenames in os.walk(path):
                for name in filenames:
                    files.append(os.path.join(root, name))
        else:
            for name in os.listdir(path):
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    files.append(full_path)
    else:
        print(f'Skip: "{target}"')

    return files


def decode_single_file(
    input_path: str,
    keep_file: bool,
    key_xz_path: str = "kugou_key.xz"
) -> bool:
    try:
        f_in = open(input_path, "rb")
    except Exception as err:
        print(f'Skip: "{input_path}", {err}')
        return False

    decoder = KuGouDecoder.try_new(f_in, key_xz_path)
    if decoder is None:
        f_in.close()
        print(f'Skip: "{input_path}"')
        return False

    try:
        head_buffer = decoder.read(128)
        if len(head_buffer) != 128:
            print(f'Skip: "{input_path}", 文件过短')
            return False

        ext = detect_audio_format(head_buffer)
        output_path = os.path.splitext(input_path)[0] + "." + ext

        if os.path.exists(output_path):
            if not confirm(f'File "{output_path}" already exists. Overwrite?'):
                return False

        try:
            f_out = open(output_path, "wb")
        except Exception as err:
            print(f'Unable to create file "{output_path}", {err}')
            return False

        try:
            f_out.write(head_buffer)

            while True:
                chunk = decoder.read(READ_BUFFER_SIZE)
                if not chunk:
                    break
                f_out.write(chunk)
        finally:
            f_out.close()

        if not keep_file:
            try:
                os.remove(input_path)
            except Exception as err:
                print(f'Warning: Unable to delete file "{input_path}", {err}')

        print(f'Ok  : "{input_path}"')
        return True

    finally:
        f_in.close()


def decode_batch(target: str, recursive: bool, keep_file: bool, key_xz_path: str) -> int:
    files = get_all_files(target, recursive)
    print(f"{len(files)} files found")

    success = 0
    for file in files:
        if decode_single_file(file, keep_file, key_xz_path):
            success += 1

    print(f"Completed {success}/{len(files)}")
    return success


def main():
    import sys
    if len(sys.argv) == 1:
        default_target = r"C:\Users\57101\OneDrive\Desktop\新建文件夹"
        decode_batch(default_target, recursive=True, keep_file=True, key_xz_path="kugou_key.xz")
        return

    parser = argparse.ArgumentParser(
        description="KGM 音频批量解密工具",
        epilog="仅用于个人合法备份的音频解密，请勿用于盗版传播"
    )
    parser.add_argument("target", help="待处理的目标文件或文件夹路径")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录中的文件")
    parser.add_argument("-k", "--keep-file", action="store_true", help="保留原始文件，不解密后删除")
    parser.add_argument("--key", default="kugou_key.xz", help="公钥xz文件路径，默认 kugou_key.xz")

    args = parser.parse_args()
    decode_batch(args.target, args.recursive, args.keep_file, args.key)


if __name__ == "__main__":
    main()
