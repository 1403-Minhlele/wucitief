from PIL import Image

filename = "Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png"
img = Image.open(filename).convert("RGB")
width, height = img.size

extracted_bits = []

for y in range(height):
    for x in range(width):
        r, g, b = img.getpixel((x, y))
        # Lấy bit MSB (bit thứ 7) của từng kênh R, G, B
        extracted_bits.append((r >> 7) & 1)
        extracted_bits.append((g >> 7) & 1)
        extracted_bits.append((b >> 7) & 1)

# Ghép các bit thành bytes
byte_array = bytearray()
for i in range(0, len(extracted_bits) - 7, 8):
    byte_val = 0
    for b in extracted_bits[i:i+8]:
        byte_val = (byte_val << 1) | b
    byte_array.append(byte_val)

# Ghi ra file để kiểm tra định dạng
with open("extracted_msb.bin", "wb") as f:
    f.write(byte_array)

print("[+] Đã trích xuất xong dữ liệu MSB!")

# Tìm flag trực tiếp nếu là plain text
if b"picoCTF{" in byte_array:
    start = byte_array.find(b"picoCTF{")
    end = byte_array.find(b"}", start) + 1
    print("[+] Flag tìm thấy:", byte_array[start:end].decode("ascii", errors="ignore"))
else:
    print("[-] Không thấy flag thô trực tiếp, kiểm tra file extracted_msb.bin bằng lệnh: file extracted_msb.bin")