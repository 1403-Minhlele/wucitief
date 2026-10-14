#!/usr/bin/env python3

import math
from pathlib import Path

INPUT_FILE = Path("1.txt.FileSlack")
OUTPUT_FILE = Path("slack_decoded.txt")


def decode_phinary(chunk, phi):
    integer_part, fractional_part = chunk.split(".")

    value = 0.0

    # Phần nguyên: các lũy thừa không âm của phi
    for i, bit in enumerate(reversed(integer_part)):
        if bit == "1":
            value += phi ** i

    # Phần phân số: các lũy thừa âm của phi
    for i, bit in enumerate(fractional_part, start=1):
        if bit == "1":
            value += phi ** (-i)

    return math.ceil(value)


def main():
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(INPUT_FILE)

    raw = INPUT_FILE.read_bytes()

    # File slack có vùng NUL ở cuối.
    # Chỉ lấy phần dữ liệu ASCII đứng trước NUL đầu tiên.
    encoded = raw.split(b"\x00", 1)[0].decode("ascii")

    if len(encoded) != 1905:
        raise ValueError(
            f"Độ dài dữ liệu không như dự kiến: {len(encoded)}"
        )

    if any(ch not in "01." for ch in encoded):
        raise ValueError("Dữ liệu chứa ký tự ngoài 0, 1 và dấu chấm.")

    if len(encoded) % 15 != 0:
        raise ValueError("Dữ liệu không chia hết thành khối 15 ký tự.")

    chunks = [
        encoded[i:i + 15]
        for i in range(0, len(encoded), 15)
    ]

    phi = (1 + math.sqrt(5)) / 2
    result = []

    for index, chunk in enumerate(chunks, start=1):
        if chunk.count(".") != 1:
            raise ValueError(
                f"Khối {index} không có đúng một dấu chấm: {chunk}"
            )

        integer_part, fractional_part = chunk.split(".")

        if len(integer_part) != 11 or len(fractional_part) != 3:
            raise ValueError(f"Cấu trúc khối {index} không hợp lệ.")

        value = decode_phinary(chunk, phi)

        if not 0 <= value <= 127:
            raise ValueError(
                f"Khối {index} tạo mã ASCII ngoài phạm vi: {value}"
            )

        result.append(chr(value))

    decoded = "".join(result)

    OUTPUT_FILE.write_text(decoded, encoding="ascii")

    print("[+] Decoded text:")
    print(decoded)
    print(f"\n[+] Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
