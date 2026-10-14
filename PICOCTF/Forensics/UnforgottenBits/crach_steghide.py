#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Test candidate passwords against a Steghide file."
    )
    parser.add_argument("image", help="Image containing embedded data")
    parser.add_argument("wordlist", help="One candidate password per line")
    parser.add_argument(
        "--output",
        default="extracted_payload.bin",
        help="Output path for extracted data",
    )
    args = parser.parse_args()

    image = Path(args.image)
    wordlist = Path(args.wordlist)

    if not image.is_file():
        sys.exit(f"[!] Không tìm thấy file ảnh: {image}")
    if not wordlist.is_file():
        sys.exit(f"[!] Không tìm thấy wordlist: {wordlist}")

    try:
        with wordlist.open("r", encoding="utf-8", errors="ignore") as f:
            passwords = [
                line.strip()
                for line in f
                if line.strip()
            ]
    except OSError as exc:
        sys.exit(f"[!] Không đọc được wordlist: {exc}")

    print(f"[*] Số mật khẩu cần thử: {len(passwords)}")

    for index, password in enumerate(passwords, start=1):
        result = subprocess.run(
            [
                "steghide", "extract",
                "-sf", str(image),
                "-p", password,
                "-xf", args.output,
                "-f",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        if result.returncode == 0 and Path(args.output).is_file():
            print(f"\n[+] Tìm thấy mật khẩu: {password}")
            print(f"[+] Dữ liệu trích xuất: {args.output}")
            return

        if index % 100 == 0 or index == len(passwords):
            print(f"[*] Đã thử {index}/{len(passwords)}", end="\r")

    print("\n[-] Không tìm thấy mật khẩu trong wordlist.")


if __name__ == "__main__":
    main()