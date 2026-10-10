# [Write-up] Steganography - MSB

## 1. Thông tin thử thách
- **Category:** Forensics / Steganography
- **File cung cấp:** `Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png`
- **Hint:** *What's causing the 'corruption' of the image?*

---

## 2. Phân tích ban đầu (Triage & Reconnaissance)

Khi nhận file ảnh, thực hiện kiểm tra sơ bộ bằng các công cụ quen thuộc:
- **`file` / `exiftool`:** Định dạng chuẩn PNG, không có metadata hoặc EXIF bất thường.
- **`pngcheck`:** Cấu trúc chunk và CRC32 hợp lệ, không có dữ liệu chèn sau `IEND` (overlay).
- **`zsteg`:** Không tìm thấy payload ở các kênh LSB (Least Significant Bit) thông thường.
- **Mở ảnh trực quan:** Khoảng 80% diện tích phía trên của ảnh bị nhiễu hạt màu (color noise/pixel noise), trong khi phần dưới hiển thị bình thường.

---

## 3. Xác định nguyên nhân & Hướng giải

### 3.1. Phân tích gợi ý
- **Gợi ý của đề bài:** *"What's causing the 'corruption' of the image?"* (Điều gì gây ra sự hỏng hóc/nhiễu hạt của bức ảnh?)
- **Tên thử thách / Thư mục:** **MSB** (Most Significant Bit - Bit có trọng số lớn nhất).

### 3.2. Cơ chế kỹ thuật
- **LSB Steganography (Bit 0):** Thay đổi bit thấp nhất chỉ làm giá trị màu lệch $\pm 1$, mắt người không phân biệt được.
- **MSB Steganography (Bit 7):** Thay đổi bit cao nhất sẽ làm giá trị màu lệch $\pm 128$. Do đó, việc nhúng dữ liệu vào bit MSB sẽ làm biến dạng màu sắc nghiêm trọng, tạo ra hiện tượng "nhiễu hạt" (noise) như nhìn thấy ở 80% phần trên của ảnh. Phần dưới cùng còn nguyên vẹn là do payload đã hết, các bit gốc được giữ nguyên.

---

## 4. Khai thác & Trích xuất (Exploitation)

Ta viết script Python sử dụng thư viện `Pillow` để:
1. Đọc từng pixel theo thứ tự quét dòng (từ trái qua phải, từ trên xuống dưới).
2. Lấy bit thứ 7 (MSB) của từng kênh màu theo thứ tự `R -> G -> B`.
3. Ghép các bit thành chuỗi byte hoàn chỉnh.

### Script trích xuất (`solve.py`):

```python
from PIL import Image

def solve(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    print(f"[*] Processing image: {width}x{height}")

    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            # Trích xuất bit thứ 7 (MSB) của từng kênh màu
            bits.append((r >> 7) & 1)
            bits.append((g >> 7) & 1)
            bits.append((b >> 7) & 1)

    # Đóng gói các bit thành byte
    extracted_bytes = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        extracted_bytes.append(byte)

    # Lưu ra file nhị phân
    with open("extracted_msb.txt", "wb") as f:
        f.write(extracted_bytes)

    print("[+] Extracted data saved to extracted_msb.txt")

    # Tìm kiếm flag trong dữ liệu giải mã
    if b"academy{" in extracted_bytes:
        start = extracted_bytes.find(b"academy{")
        end = extracted_bytes.find(b"}", start) + 1
        print("[+] Flag found:", extracted_bytes[start:end].decode("ascii", errors="ignore"))

if __name__ == "__main__":
    solve("Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png")